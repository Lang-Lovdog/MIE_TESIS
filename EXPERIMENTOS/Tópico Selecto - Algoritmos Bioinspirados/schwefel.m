function f = schwefel(x1, x2)
  salida=0;
  if x1 >= -500 && x1 <= 500
    salida = salida-x1*sin(sqrt(abs(x1)));
  else
      salida = salida+0.02*x1*x1;
  end
  if x2 >= -500 && x2 <= 500
    salida = salida-x2*sin(sqrt(abs(x2)));
  else
      salida = salida+0.02*x2*x2;
  end
  f = 418.9829 + salida;
end
