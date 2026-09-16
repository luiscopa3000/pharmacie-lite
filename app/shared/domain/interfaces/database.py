from typing import Protocol, Any, Dict, Tuple, runtime_checkable, List, Optional

@runtime_checkable
class ISqlDatabase(Protocol):
    def execute_query_string(
        self,
        query_string: str,
        params: Tuple = (),
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
        current_user_id: Optional[str] = None,
    ) -> Any:
        """
        Ejecuta una consulta SQL con parámetros seguros.

        Parámetros:
            query_string (str): La consulta SQL con placeholders (%s).
            params (tuple): Tupla con los valores para los placeholders en la consulta.

        Retorna:
            list[tuple]: Resultado de la consulta como lista de tuplas.
        """
        ...


    def execute_query_dynamic(
        self, 
        query_name: str,
        obj: Any,
        *,
        request_id: Optional[str] = None,
        host: Optional[str] = None,
        current_user_id: Optional[str] = None,
    ) -> List[Dict]:
        """
        Ejecuta una función SQL dinámica recibiendo cualquier objeto y el nombre del query.
        Convierte el objeto a dict si es necesario.
        Si no se recibe query_name, lo toma del atributo 'query' del objeto.
        Si el objeto no tiene 'parameters', lo envuelve en {'query':..., 'parameters':...}
        """
        ...