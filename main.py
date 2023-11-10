from fastapi import FastAPI, Body
from simplex import Simplex
import ast

app = FastAPI()

# class body:
#     n_variables: int
#     obj_funct : Tuple[str,Tuple[int]]
#     restrictions = List[Tuple[Tuple[int],str,int]]

@app.get("/")
def standard_model(body: dict = Body(...)):
    n_variables = body["n_variables"]

    obj_funct = ast.literal_eval(body["obj_funct"])
    restrictions = ast.literal_eval(body["restrictions"])

    solver = Simplex(n_variables, obj_funct, restrictions)
    return {"X":solver.x, "C":solver.C, "b":solver.b, "A":solver.A.tolist()}