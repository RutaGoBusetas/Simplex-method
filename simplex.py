import numpy as np

class Simplex():

    def __init__(self, n_var, obj_funct, rest):
        self.n_var = n_var
        self.obj_funct = obj_funct
        self.rest = rest        
        self.z = 0

        # index 0 referes to s value and index 1 referes to m value
        self.ineq = {
            "=":(0,1),
            "<=": (1,0),
            ">=": (-1,1)
        }

        self.A, self.C = [],[]
        self.b = [r[-1] for r in self.rest]
        self.x = ["x"+str(i+1) for i in range(self.n_var)]
        self.fill_A_C()
        self.A = np.array(self.A)
        # print('A matrix:')
        # print(self.A)
        # print(f'C vector: {self.C}\n')

        prob = obj_funct[0].lower()
        if prob == "min": self.max = False
        elif prob == "max": self.max = True
        else: raise Exception("Unknown procedure")

    def fill_A_C(self):
        params_value,s_values, m_values = [], [],[]
        for rest in self.rest:
            ineq = self.ineq[rest[1]]

            params_value.append([param for param in rest[0]])
            if ineq[0] == 0: s_values.append(None)
            else: s_values.append(ineq[0])

            if ineq[1] == 0: m_values.append(None)
            else: m_values.append(ineq[1]*rest[-1])

        for i in range(len(self.rest)):
            self.A.append(
                params_value[i]+
                [s_values[j] if i==j else 0 for j in range(len(s_values)) if s_values[j] is not None]+
                [1 if i==j else 0 for j in range(len(m_values)) if m_values[j] is not None]
            )
        
        self.C = [value for value in self.obj_funct[-1]] + [0 for value in s_values if value is not None] + [-800 for value in m_values if value is not None]
        self.x.extend("S"+str(i) for i in range(len(s_values)) if s_values[i] is not None)
        self.x.extend("u"+str(i) for i in range(len(m_values)) if m_values[i] is not None)

    def solve(self):
        X_b = [] 
        for row in range(len(self.A)):
            for col in range(len(self.A[row])):
                if self.A[row][col] == 1:
                    identity = True
                    for r in range(len(self.A)):
                        if r != row and self.A[r][col] != 0:
                            identity = False
                            break
                    if identity: 
                        X_b.append(col)
                        break
        
        iter = 0
        while(True):
            print('-'*100)
            print(f'iter {iter}')
            print('-'*100)
            print(f'basic variables vector: {X_b}')
            C_b = [self.C[i] for i in X_b]
            B = self.A[:,X_b]

            print(f'basic cost vector: {C_b}')
            print('basic matrix:')
            print(B)

            inv_B= np.linalg.inv(B)
            invB_A = np.dot(inv_B, self.A)
            Cb_invB_A = np.dot(C_b,invB_A)
            r = np.round(Cb_invB_A-self.C,4)
            print(f'\nCb_invB_A: {Cb_invB_A}')
            print(f'r: {r}')

            z = np.dot((np.dot(np.transpose(C_b),inv_B)),self.b)
            print(f'z value: {z}')


            invB_b = np.dot(inv_B, self.b)
            
            
            if self.max:
                if not any(r<0):
                    break
                else:
                    in_var = np.argmin(r)
                    aux = invB_A[:,in_var]
                    out_var = np.nanargmin(np.divide(invB_b,aux, out=np.full_like(invB_b, np.nan), where=aux>0))
            else:
                if not any(r>0):
                    break
                else:
                    in_var = np.argmax(r)
                    aux = invB_A[:,in_var]
                    # print(invB_b)
                    # print(aux)
                    # print(np.divide(invB_b,aux, out=np.full_like(invB_b, np.nan), where=aux>0 ))
                    out_var = np.nanargmax(np.divide(invB_b,aux, out=np.full_like(invB_b, np.nan), where=aux<0 ))

            print(f'out var: {out_var}')
            print(f'in var: {in_var}')
            X_b[out_var] = in_var
            iter+=1

        result = [invB_b[i] for i in range(len(X_b)) if X_b[i] in range(self.n_var)]
        return result
        




if __name__ == '__main__':
    # params = {
    #     'p1':1000,
    #     'p2':1120,
    #     'p3':900,
    #     't1':1,
    #     't2':1.2,
    #     't3':0.8,
    #     'f':20,
    #     'm1':8,
    #     'm2':0,
    #     'm3':5
    # }

    # n_variables = 3

    # obj_funct = ('max',(params['p1'], params['p2'], params['p3']))

    # restrictions = [
    #     # ((1,0,0),'>=', 0) , ((0,1,0),'>=', 0), ((0,0,1),'>=', 0),
    #     ((params['t1'],params['t2'],params['t3']),'<=',params['f']),
    #     ((1,0,0),'>=', params['m1']), 
    #     ((0,1,0),'>=', params['m2']),
    #     ((0,0,1),'>=', params['m3'])
    # ]

    ################################

    n_variables = 2

    obj_funct = ('max',(5, 8))
    restrictions = [
        ((6,5), '<=',30),
        ((0,1), '>=', 1),
        ((-2,2), '<=', 6)
    ]

    solver = Simplex(n_variables, obj_funct, restrictions)
    # print(solver.)
    print(f'\n\nsolution: {solver.solve()}')