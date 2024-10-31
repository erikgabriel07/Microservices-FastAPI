from functools import wraps
from fastapi import HTTPException
from fastapi import status as s



def verify_id_parameter(f):
    
    @wraps(f)
    async def decorator(*args, **kwargs):
        id = kwargs.get('id') # Recupera o ID passado para a rota

        if not id:
            # Se nenhum ID for fornecido, lança uma exceção
            raise HTTPException(
                status_code=s.HTTP_400_BAD_REQUEST,
                detail={'message': 'Nenhum ID foi fornecido!'}
            )
        return await f(*args, **kwargs)
    
    return decorator