from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import math

mcp = FastMCP("Math Tutor")

class ResultadoEcuacion(BaseModel):
    solucion: str = Field(description="Resultado de la ecuación o expresión")

@mcp.tool("resolver_ecuacion_lineal")
def resolver_ecuacion_lineal(a: float, b: float) -> ResultadoEcuacion:
    """
    Resuelve una ecuación lineal de la forma ax + b = 0
    Args:
        a: Coeficiente principal
        b: Término independiente
    """
    try:
        if a == 0:
            return ResultadoEcuacion(solucion="No hay solución (a=0)")
        x = -b / a
        return ResultadoEcuacion(solucion=f"x = {x}")
    except Exception as e:
        return ResultadoEcuacion(solucion=f"Error: {e}")

@mcp.tool("resolver_ecuacion_cuadratica")
def resolver_ecuacion_cuadratica(a: float, b: float, c: float) -> ResultadoEcuacion:
    """
    Resuelve una ecuación cuadrática ax² + bx + c = 0
    Args:
        a: Coeficiente cuadrático
        b: Coeficiente lineal
        c: Término independiente
    """
    try:
        if a == 0:
            return ResultadoEcuacion(solucion="No es cuadrática (a=0)")
        disc = b**2 - 4*a*c
        if disc < 0:
            return ResultadoEcuacion(solucion="No hay raíces reales")
        x1 = (-b + math.sqrt(disc)) / (2*a)
        x2 = (-b - math.sqrt(disc)) / (2*a)
        return ResultadoEcuacion(solucion=f"x₁={x1}, x₂={x2}")
    except Exception as e:
        return ResultadoEcuacion(solucion=f"Error: {e}")

@mcp.tool("realizar_operacion")
def realizar_operacion(expresion: str) -> ResultadoEcuacion:
    """
    Evalúa una expresión matemática (por ejemplo: "2*3+5").
    Args:
        expresion: Expresión matemática en formato string.
    """
    try:
        resultado = eval(expresion)
        return ResultadoEcuacion(solucion=f"Resultado: {resultado}")
    except Exception as e:
        return ResultadoEcuacion(solucion=f"Error en la expresión: {e}")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
