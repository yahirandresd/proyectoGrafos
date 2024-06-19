def intento_atraco(escudo_ladrones, ataque_ladrones, escudo_escoltas, ataque_escoltas, escudo_carro, ataque_carro):

    if escudo_carro == 20:
        poder_ataque_ladrones = ataque_ladrones
        poder_defensa_escoltas = (escudo_escoltas*2) + escudo_carro
        poder_ataque_escoltas = (ataque_escoltas*2) + ataque_carro
        poder_defensa_ladrones = escudo_ladrones
    else:
        poder_ataque_ladrones = ataque_ladrones
        poder_defensa_escoltas = escudo_escoltas + escudo_carro
        poder_ataque_escoltas = ataque_escoltas + ataque_carro
        poder_defensa_ladrones = escudo_ladrones

    print(f"Ataque Escoltas: {poder_ataque_escoltas}")
    print(f"Defensa Escoltas: {poder_defensa_escoltas}")
    print()
    print(f"Ataque LADRONES: {poder_ataque_ladrones}")
    print(f"Defensa LADRONES: {poder_defensa_ladrones}")
    # Determina el resultado del enfrentamiento
    if poder_ataque_ladrones > poder_defensa_escoltas:
        resultado = "Los ladrones han logrado el atraco!"
    elif poder_ataque_escoltas > poder_defensa_ladrones:
        resultado = "Los escoltas han repelido el ataque exitosamente!"
    else:
        resultado = "El ataque ha sido repelido, pero con grandes pérdidas de escudo para ambos lados."

    return resultado