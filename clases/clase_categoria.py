class clsproducto:
    id = 0
    producto = ""
    dicproducto = {}

    def __init__(self,p_id,p_producto):
        self.id = p_id
        self.producto = p_producto
        self.dicproducto={
            "id": p_id,
            "producto"  : p_producto
        } 