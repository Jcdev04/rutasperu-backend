import heapq
from collections import defaultdict
from firebase_admin import firestore


class BuscadorRutas:
    def __init__(self, datos_rutas):
        """
        datos_rutas: lista de dicts tal como doc.to_dict() de Firestore
        Cada dict debe tener las claves:
        - origen (str)
        - destino (str)
        - precio_soles (float)
        - duracion_min (int)
        - id (str)
        """
        self.datos_rutas = datos_rutas
        self.grafo = defaultdict(list)
        self._construir_grafo_bidireccional()

    def _construir_grafo_bidireccional(self):
        for ruta in self.datos_rutas:
            o = ruta["origen"]
            d = ruta["destino"]
            p = ruta["precio_soles"]
            t = ruta["duracion_min"]
            uid = ruta["id"]
            # ida
            self.grafo[o].append((d, p, t, uid))
            # vuelta
            self.grafo[d].append((o, p, t, uid))

    def _validar_distritos(self, *distritos):
        for dis in distritos:
            if dis not in self.grafo:
                raise ValueError(f"Distrito {dis} no existe en el grafo")

    def buscar_ruta_optima(self, origen, destino):
        self._validar_distritos(origen, destino)

        dist = {n: float("inf") for n in self.grafo}
        dist[origen] = 0
        prev = {n: None for n in self.grafo}
        prev_ruta = {n: None for n in self.grafo}
        tiempo = {n: 0 for n in self.grafo}
        pq = [(0, origen)]

        while pq:
            costo_actual, nodo = heapq.heappop(pq)
            if nodo == destino:
                break
            if costo_actual > dist[nodo]:
                continue

            for vecino, precio, dur, uid in self.grafo[nodo]:
                nuevo = costo_actual + precio
                if nuevo < dist[vecino]:
                    dist[vecino] = nuevo
                    prev[vecino] = nodo
                    prev_ruta[vecino] = uid
                    tiempo[vecino] = tiempo[nodo] + dur
                    heapq.heappush(pq, (nuevo, vecino))

        if prev[destino] is None and origen != destino:
            raise ValueError(f"No hay ruta entre {origen} y {destino}")

        # reconstruir ruta y recoger pasos
        pasos_ids = []
        cur = destino
        while cur:
            if prev_ruta[cur]:
                pasos_ids.insert(0, prev_ruta[cur])
            cur = prev[cur]

        # convertir cada id de ruta en el objeto completo
        steps = [self.obtener_detalle_ruta(uid) for uid in pasos_ids]

        return {
            "total": dist[destino],
            "steps": steps
        }

    def obtener_detalle_ruta(self, id_ruta):
        return next((r for r in self.datos_rutas if r["id"] == id_ruta), None)

    def obtener_distritos_conectados(self, distrito):
        self._validar_distritos(distrito)
        return [v[0] for v in self.grafo[distrito]]
