from fastapi import FastAPI, Body
from simplex import Simplex
from fastapi.middleware.cors import CORSMiddleware
import ast

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# class body:
#     n_variables: int
#     obj_funct : Tuple[str,Tuple[int]]
#     restrictions = List[Tuple[Tuple[int],str,int]]

@app.get("/")
def get_root():
    return {"Simplex method":"API"}

@app.post("/")
async def standard_model(body: dict = Body(...)):
    n_variables = body["n_variables"]
    obj_funct = (body["obj_funct"]["action"],body["obj_funct"]["coefficients"])
    restrictions = body["restrictions"]
    # obj_funct = ast.literal_eval(body["obj_funct"])
    # restrictions = ast.literal_eval(body["restrictions"])
    print("N_variables: ",n_variables, "   Type: ",type(n_variables))
    print("obj_funct: ",obj_funct, "    Type: ",type(obj_funct))
    print("restricciones: ",restrictions, "    Type: ",type(restrictions))
    solver = Simplex(n_variables, obj_funct, restrictions)
    return {"X":solver.x, "C":solver.C, "b":solver.b, "A":solver.A.tolist()}

# ('max',(5, 8))
# [((6,5), '<=',30),((0,1), '>=', 1),((-2,2), '<=', 6)]