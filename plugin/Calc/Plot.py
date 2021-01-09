import base64
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application
from sympy import parse_expr,latex,evaluate,latex,Eq,solve,factor,plot
from PIL import Image
import io
import matplotlib
import sys
raw = eval(base64.b64decode(sys.argv[1].encode()).decode())
arr = [parse(x) for x in raw[0]]
symbol = parse(raw[1])
axis = raw[2]
xlabel = raw[3]
ylabel = raw[4]
transformations = (standard_transformations + (implicit_multiplication_application,))
def parse(s, e=True):
    return parse_expr(s, transformations=transformations, evaluate = e)
p1 = plot(arr[0], (symbol, -axis, axis), xlabel = xlabel, ylabel = ylabel, show=False)
[p1.append(plot(arr[x7], (symbol, -axis, axis), xlabel = xlabel, ylabel = ylabel, show=False)[0]) for x7 in range(1, len(arr))]
iobuff= io.BytesIO()
p1.save(iobuff)
print(base64.b64encode(repr(['资讯: \n'+str(p1)+'\n[PICFLAG]', base64.b64encode(iobuff.getvalue()).decode()]).encode()).decode())
