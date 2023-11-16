from fastapi import FastAPI, Body, HTTPException
from simplex import Simplex
import os
from fastapi.middleware.cors import CORSMiddleware
import ast

port = int(os.getenv("PORT", 8000))
app = FastAPI()
solver = None
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def get_root():
    return {"Simplex method":"API"}

@app.post("/")
async def standard_model(body: dict = Body(...)):
    n_variables = body["n_variables"]
    obj_funct = (body["obj_funct"]["action"],body["obj_funct"]["coefficients"])
    restrictions = body["restrictions"]

    global solver
    solver = Simplex(n_variables, obj_funct, restrictions)
    return {"X":solver.x, "C":solver.C, "b":solver.b, "A":solver.A.tolist()}

@app.get("/solution")
def get_solution():
    if solver is None:
        raise HTTPException(status_code=404, detail="Object not found")
    
    solucion = solver.solve()
    if isinstance(solucion, dict):
        special_case = "Sin caso especial"
    else:
        soluciones = {-1: "Punto degenerado", -2: "Múltiples soluciones", -3: "Solución no acotada", -4: "Incompatibilidad"}
        special_case = soluciones.get(solucion, "Sin caso especial")
    iterations = len(solver.iterations)
    print(solver.iterations)
    X_b = [[solver.x[i] for i in iteration[0]] for iteration in solver.iterations]
    Z = [iteration[1] for iteration in solver.iterations]
    invB_b = [iteration[2] if iteration[2] is None else iteration[2].tolist() for iteration in solver.iterations]
    r = [iteration[3] if iteration[3] is None else iteration[3].tolist() for iteration in solver.iterations]
    iterando = [iteration[4] for iteration in solver.iterations]
    in_var = [iteration[5] if iteration[5] is None else solver.x[iteration[5]] for iteration in solver.iterations]
    out_var = [iteration[6] if iteration[6] is None else solver.x[iteration[0][iteration[6]]] for iteration in solver.iterations]
    return {"num_iters": iterations, "iterations": {
        "X_b":X_b, "Z":Z, "InvB_b":invB_b, "r":r, "iterando":iterando,
        "in_var":in_var, "out_var": out_var}, "special_case":special_case}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
# BODY:
# {
#   "n_variables" : 2,
#   "obj_funct" : {
#     "action":"max",
#     "coefficients": [5,8]
#   },
#   "restrictions" : [[[6,5], "<=",30],[[0,1], ">=", 1],[[-2,2], "<=", 6]]
# }

# - Variables solución en ese punto: Es X_B
# - Solución del modelo en esa iteración: Es Z
# - Solución de las variables es: B^-1*b
# - Vector de costos reducidos: r
# - Indicar si se sigue iterando o no   
# - Variable que entra y la que sale
# - Muestre qué caso especial es
