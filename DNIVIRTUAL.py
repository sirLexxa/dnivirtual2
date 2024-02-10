def dnivir_menores(dni):
    import cv2
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageFilter
    import requests
    import base64
    from io import BytesIO
    import numpy as np
    import random
                
    url = "https://api.ddosis.fun/reniec?token=NjWzldwgBYlbShDPwIEGkZZkvfn&dni="+ dni

    response = requests.get(url)
    resultado = response.json()

    if resultado == "El DNI no se encuentra registrado en la Base de Datos de Reniec":
        return resultado
    elif resultado == "EL SERVICIO DE RENIEC ESTA EN MANTENIMIENTO":
        return resultado
    else:
        datos = resultado['listaAni'][0]
        
        url2 = "https://ubis-gustavxrossi.replit.app/consulta?distrito="+ datos["distrito"]
        
        response = requests.get(url2)
        resultado2 = response.json()

        apellido_paterno = datos["apePaterno"]
        apellido_paterno2 = datos["apePaterno"] + '<<' + datos["preNombres"].replace(" ", "<",)
        apellido_materno = datos['apeMaterno']
        nombres = datos['preNombres']
        dni = datos['nuDni']
        sexo = datos['sexo'][0]
        dni1 = dni + '<' + str(random.randint(0, 9))
        caducidad = datos["feCaducidad"].replace("/", " ")
        emision = datos["feEmision"].replace("/", " ")
        digitoverfi = datos["digitoVerificacion"]
        inscripcion = datos["feInscripcion"].replace("/", " ")
        fenacimiento = datos["feNacimiento"].replace("/", " ")
        fenacimiento2 = datos["feNacimiento"][8]+datos["feNacimiento"][9]+datos["feNacimiento"][3]+datos["feNacimiento"][4]+datos["feNacimiento"][0]+datos["feNacimiento"][1]+ str(random.randint(0, 9))+datos["sexo"][0]+datos["feCaducidad"][8]+datos["feCaducidad"][9]+datos["feCaducidad"][3]+datos["feCaducidad"][4]+datos["feCaducidad"][0]+datos["feCaducidad"][1]+ str(random.randint(0, 9))+ "PER"
        
        foto = resultado['foto']
        hderecha = resultado['hderecha']

        ubigeo_nac = resultado2["ubigeo"]
        dona_organos = datos["donaOrganos"]

        foto_without_newline = foto.replace("\n", "")
        image_data = base64.b64decode(foto_without_newline)
        image_buffer1 = BytesIO(image_data)
        foto_image = Image.open(image_buffer1)

        hderecha_without_newline = hderecha.replace("\n", "")
        image_data = base64.b64decode(hderecha_without_newline)
        image_buffer2 = BytesIO(image_data)
        huella_image = Image.open(image_buffer2)

        departamente = datos["depaDireccion"]
        provincia = datos['provincia']
        distrito = datos["distDireccion"]
        direccion = datos["desDireccion"]

        madre = datos["nomMadre"]
        madre_dni = datos["nuDocMadre"]
        padre = datos["nomPadre"]
        padredni = datos["nuDocPadre"]

        PLANTILLA = Image.open("./Templates/Yellow/FRONT-AMARILLO.jpg")
        
        resized_image = foto_image.resize((410, 580))
        
        PLANTILLA.paste(resized_image, (105, 210))

        LETRA = Image.open("./Templates/LETRAFONDO.png")

        if LETRA.mode != "RGBA" and LETRA.mode != "LA":
                LETRA = LETRA.convert("RGBA")

        dibujo = ImageDraw.Draw(LETRA)
        texto = dni
        fuente = ImageFont.truetype("./Fonts/Helveticabold.ttf", size=60)

        bbox = fuente.getbbox(texto)
        ancho_total = bbox[2] - bbox[0] + 25 * (len(texto) - 1)
        alto_total = bbox[3] - bbox[1]

        caja_texto = Image.new('RGBA', (ancho_total, alto_total), (255, 255, 255, 0))
        dibujo_texto = ImageDraw.Draw(caja_texto)

        pos_x = 0
        for letra in texto:
                bbox = dibujo_texto.textbbox((pos_x, -5), letra, font=fuente)
                ancho_letra = bbox[2] - bbox[0]
                dibujo_texto.text((pos_x, -5), letra, font=fuente, fill=(156, 13, 13))
                pos_x += ancho_letra + 25

        texto_rotado = caja_texto.rotate(270, expand=True)
        LETRA.paste(texto_rotado, (0, 0), texto_rotado)

        letra_buffer = BytesIO()
        LETRA.save(letra_buffer, format="PNG")
        letra_buffer.seek(0)

        draw = ImageDraw.Draw(PLANTILLA)
        font = ImageFont.truetype("./Fonts/Helveticabold.ttf", 40)
        font1 = ImageFont.truetype("./Fonts/Helveticabold.ttf", 40)
        font2 = ImageFont.truetype("./Fonts/Helveticabold.ttf", 40)
        font3 = ImageFont.truetype("./Fonts/Helveticabold.ttf", 60)
        font4 = ImageFont.truetype("./Fonts/OCR.ttf", 105)

        draw.text((220, 773), apellido_paterno.upper(), font=font, fill=(156, 13, 13))
        draw.text((530, 250), apellido_paterno.upper(), font=font1, fill=(0, 0, 0))
        draw.text((530, 390), apellido_materno.upper(), font=font1, fill=(0, 0, 0))
        draw.text((530, 530), nombres.upper(), font=font1, fill=(0, 0, 0))
        draw.text((535, 670), fenacimiento.upper(), font=font2, fill=(0, 0, 0))
        draw.text((850, 670), ubigeo_nac.upper(), font=font2, fill=(0, 0, 0))
        draw.text((535, 760), sexo.upper(), font=font2, fill=(0, 0, 0))
        draw.text((1660, 260), inscripcion.upper(), font=font1, fill=(0, 0, 0))
        draw.text((1660, 380), emision.upper(), font=font1, fill=(0, 0, 0))
        if caducidad == "DNI NO CADUCA": 
                x_pos = 1625 
                font = ImageFont.truetype("./Fonts/Helveticabold.ttf", size=35) 
        else: 
                x_pos = 1660 
        font = ImageFont.truetype("./Fonts/Helveticabold.ttf", size=40) 
        draw.text((x_pos, 500), caducidad.upper(), font=font, fill=(156, 13, 13))
        draw.text((1550, 130), dni.upper(), font=font3, fill=(156, 13, 13))
        draw.text((1820, 130), "-" , font=font3, fill=(0, 0, 0))
        draw.text((1840, 130), digitoverfi.upper() , font=font3, fill=(0, 0, 0))
        draw.text((110, 900), "I<PER", font=font4, fill=(0, 0, 0))
        draw.text((1820, 1000), str(random.randint(0, 9)), font=font4, fill=(0, 0, 0))

        dni_sin=dni.replace(" ", "")

        texto = dni_sin+"<"+ str(random.randint(0, 9)).upper()
        max_letras = 23
        if len(texto) > max_letras:
                        texto_limitado = texto[:max_letras]
        else:
                        texto_limitado = texto.ljust(max_letras, "<")
        font4 = ImageFont.truetype("./Fonts/OCR.ttf", 105)
        fill = (0, 0, 0)

        draw.text((420, 900), texto_limitado, font=font4, fill=fill)

        texto = fenacimiento2.upper()
        max_letras = 27

        if len(texto) > max_letras:
                texto_limitado = texto[:max_letras]
        else:
                texto_limitado = texto.ljust(max_letras, "<")
        font4 = ImageFont.truetype("./Fonts/OCR.ttf", 105)
        fill = (0, 0, 0)

        draw.text((110, 1000), texto_limitado, font=font4, fill=fill)

        texto = apellido_paterno2.upper()
        max_letras = 28

        if len(texto) > max_letras:
                texto_limitado = texto[:max_letras]
        else:
                texto_limitado = texto.ljust(max_letras, "<")

        font4 = ImageFont.truetype("./Fonts/OCR.ttf", 105)
        fill = (0, 0, 0)

        draw.text((110, 1100), texto_limitado, font=font4, fill=fill)

        plantilla_buff = BytesIO()
        PLANTILLA.save(plantilla_buff, format="PNG")
        plantilla_buff.seek(0)

        img = cv2.imread('./Templates/RAYAS.png', cv2.IMREAD_UNCHANGED)

        if img.shape[2] == 4:
                has_transparency = True
        else:
                has_transparency = False

        if has_transparency:
                b, g, r, a = cv2.split(img)
                rgb_img = cv2.merge([b, g, r])
        else:
                rgb_img = img

        width = 410
        height = 580
        resized_rgb_img = cv2.resize(rgb_img, (width, height), interpolation=cv2.INTER_AREA)

        if has_transparency:
                resized_alpha = cv2.resize(a, (width, height), interpolation=cv2.INTER_AREA)
                resized_img = cv2.merge([resized_rgb_img, resized_alpha])
        else:
                resized_img = resized_rgb_img
        success, encoded_image = cv2.imencode('.png', resized_img)

        if not success:
                raise Exception("Error al codificar la imagen")
        raya2_buffer = BytesIO(encoded_image.tobytes())

        img = cv2.imdecode(np.frombuffer(letra_buffer.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        if img.shape[2] == 4:
                        has_transparency = True
        else:
                        has_transparency = False
        if has_transparency:
                        b,g,r,a = cv2.split(img)
                        rgb_img = cv2.merge([b,g,r])
        width = 450
        height = 650
        resized_rgb_img = cv2.resize(rgb_img, (width, height), interpolation=cv2.INTER_AREA)
        if has_transparency:
                        resized_alpha = cv2.resize(a, (width, height), interpolation=cv2.INTER_AREA)
        if has_transparency:
                        resized_img = cv2.merge([resized_rgb_img, resized_alpha])
        else:
                        resized_img = resized_rgb_img
        success, letra2_image = cv2.imencode('.png', resized_img)

        letra_rotada_buffer = BytesIO(letra2_image.tobytes())
        letra_rotada_buffer.seek(0)

        img = foto_image

        img = img.convert('L')
        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        img = Image.open(output_buffer).convert('RGB')
        img = img.convert('L')
        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG')
        output_buffer.seek(0)
        
        img = Image.open(output_buffer).convert('RGB')
        img = img.convert('L')
        pixdata = img.load()

        for y in range(img.size[1]):
                        for x in range(img.size[0]):
                                        if pixdata[x, y] != 0:
                                                        pixel = pixdata[x, y]
                                                        pixdata[x, y] = min(255, int(pixel * 1))
        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG')
        img = img.filter(ImageFilter.SMOOTH_MORE)
        img = img.convert('RGBA')
        pixdata = img.load()
        for y in range(img.size[1]):
                for x in range(img.size[0]):
                        if pixdata[x, y][0] > 200 and pixdata[x, y][1] > 200 and pixdata[x, y][2] > 200:
                                pixdata[x, y] = (255, 255, 255, 0)
                        elif pixdata[x, y][0] > 180 and pixdata[x, y][1] > 180 and pixdata[x, y][2] > 180:
                                pixdata[x, y] = (215, 215, 215, 0)

        imagen_sin_fondo2_buffer = BytesIO()
        img.save(imagen_sin_fondo2_buffer, format="PNG")
        imagen_sin_fondo2_buffer.seek(0)

        img = Image.open(imagen_sin_fondo2_buffer)
        enhancer = ImageEnhance.Contrast(img)
        img_con_contraste = enhancer.enhance(3.5)

        img_con_contraste_buffer = BytesIO()
        img_con_contraste.save(img_con_contraste_buffer, format='PNG')
        img_con_contraste_buffer.seek(0)

        img = Image.open(img_con_contraste_buffer)

        transparency = Image.new('RGBA', img.size, (0, 0, 0, 0))
        alpha = 0.4
        result = Image.blend(img, transparency, alpha)

        result_buffer = BytesIO()
        result.save(result_buffer, format='PNG')
        result_buffer.seek(0)

        img23 = Image.open(result_buffer)

        size = (150, 200)
        img_resized = img23.resize(size)

        img_resized_buffer = BytesIO()
        img_resized.save(img_resized_buffer, format='PNG')
        img_resized_buffer.seek(0)

        from rembg import remove
        from PIL import Image

        output_buffer.seek(0)

        img = Image.open(output_buffer)
        img = remove(img)

        imagen_con_filtro_buffer = BytesIO()
        img.save(imagen_con_filtro_buffer, format="PNG")
        imagen_con_filtro_buffer.seek(0)

        img = Image.open(imagen_con_filtro_buffer)

        img = img.convert('RGBA')
        filtro = Image.new('RGBA', img.size, (40, 85, 98, int(96 * 1.3)))

        img_con_filtro = Image.alpha_composite(img, filtro)
        img_con_filtro.putalpha(img.split()[3])

        imagen_con_filtro_buffer = BytesIO()
        img_con_filtro.save(imagen_con_filtro_buffer, format='PNG')
        imagen_con_filtro_buffer.seek(0)

        img = Image.open(imagen_con_filtro_buffer)
        enhancer = ImageEnhance.Contrast(img)
        img_con_contraste = enhancer.enhance(3.5)

        foto_mini_buffer = BytesIO()
        img_con_contraste.save(foto_mini_buffer, format='PNG')
        foto_mini_buffer.seek(0)

        img = Image.open(foto_mini_buffer)

        transparency = Image.new('RGBA', img.size, (0, 0, 0, 0))
        alpha = 0.5
        result = Image.blend(img, transparency, alpha)

        foto_mini_buffer = BytesIO()
        result.save(foto_mini_buffer, format='PNG')
        foto_mini_buffer.seek(0)

        img23 = Image.open(foto_mini_buffer)

        size = (150, 200)
        img_resized = img23.resize(size)

        foto_mini_buffer = BytesIO()
        img_resized.save(foto_mini_buffer, format='PNG')
        foto_mini_buffer.seek(0)

        imagen_jpg = Image.open(plantilla_buff)
        imagen_mini = Image.open(foto_mini_buffer)
        imagen_lineas = Image.open(raya2_buffer)

        imagen_texto = Image.open(letra_rotada_buffer)
        imagen_mini2 = Image.open(img_resized_buffer)

        dni_frontal = Image.new('RGB', imagen_jpg.size, (255, 255, 255))
        dni_frontal.paste(imagen_jpg, (0, 0))
        dni_frontal.paste(imagen_mini2, (1710, 640), imagen_mini2)
        dni_frontal.paste(imagen_mini, (1710, 640), imagen_mini)
        dni_frontal.paste(imagen_lineas, (105, 210), imagen_lineas)
        dni_frontal.paste(imagen_texto, (80, 240), imagen_texto)

        from PIL import Image, ImageDraw, ImageFont

        REVERSO= Image.open(f'./Templates/Yellow/BACK-AMARILLO.jpg')

        background = Image.open(f'./Templates/Yellow/BACK-AMARILLO.jpg')

        new_size = (310, 420)
        resized_image = huella_image.resize(new_size)

        background.paste(resized_image, (1550, 43))

        draw = ImageDraw.Draw(background)
        font1 = ImageFont.truetype("./Fonts/Helveticabold.ttf", 40)
        font2 = ImageFont.truetype("./Fonts/Helveticabold.ttf", 50)

        palabras = madre.split()

        if len(palabras) >= 1:
            palabra1 = palabras[0]
        else:
            palabra1 = ""
        if len(palabras) >= 2:
            palabra2 = palabras[1]
        else:
            palabra2 = ""
        if len(palabras) > 2:
            palabra3 = " ".join(palabras[2:])
        else:
            palabra3 = ""
        palabras_padre = padre.split()
        if len(palabras_padre) >= 1:
            palabra_padre_1 = palabras_padre[0]
        else:
            palabra_padre_1 = ""
        if len(palabras_padre) >= 2:
            palabra_padre_2 = palabras_padre[1]
        else:
            palabra_padre_2 = ""
        if len(palabras_padre) > 2:
            palabra_padre_3 = " ".join(palabras_padre[2:])
        else:
            palabra_padre_3 = ""

        draw.text((230, 80), palabra1, font=font1, fill=(0, 0, 0))
        draw.text((230, 130), palabra2, font=font1, fill=(0, 0, 0))
        draw.text((230, 180), palabra3, font=font1, fill=(0, 0, 0))
        
        draw.text((400, 232), madre_dni, font=font1, fill=(0, 0, 0))

        draw.text((230, 300), palabra_padre_1, font=font1, fill=(0, 0, 0))
        draw.text((230, 350), palabra_padre_2, font=font1, fill=(0, 0, 0))
        draw.text((230, 400), palabra_padre_3, font=font1, fill=(0, 0, 0))
        
        draw.text((400, 452), padredni , font=font1, fill=(0, 0, 0))

        draw.text((80, 570), direccion , font=font1, fill=(0, 0, 0))

        draw.text((80, 735), distrito , font=font1, fill=(0, 0, 0))
        draw.text((670, 735), provincia , font=font1, fill=(0, 0, 0))
        draw.text((1310, 735), departamente , font=font1, fill=(0, 0, 0))

        frontal_buffer = BytesIO()
        posterior_buffer = BytesIO()

        dni_frontal.save(frontal_buffer, format='JPEG')
        background.save(posterior_buffer, format='JPEG')

        frontal_base64 = base64.b64encode(frontal_buffer.getvalue()).decode('utf-8')
        posterior_base64 = base64.b64encode(posterior_buffer.getvalue()).decode('utf-8')

        frontal_buffer.seek(0)
        posterior_buffer.seek(0)

        return {'posterior_base64': frontal_base64, 'frontal_base64': posterior_base64, 'datos': resultado["listaAni"]}

def dnivir(dni):
    import cv2
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageFilter
    import requests
    import base64
    import numpy as np
    import random
    from io import BytesIO
    import cv2
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageFilter
    import requests
    import base64
    from io import BytesIO
    import numpy as np
    import random
                
    try:
        url = "https://api.ddosis.fun/reniec?token=NjWzldwgBYlbShDPwIEGkZZkvfn&dni="+ dni

        response = requests.get(url)
        resultado = response.json()
    except Exception as e:
        resultado = "EL SERVICIO DE RENIEC ESTA EN MANTENIMIENTO"

    if resultado == "El DNI no se encuentra registrado en la Base de Datos de Reniec":
        return resultado
    elif resultado == "EL SERVICIO DE RENIEC ESTA EN MANTENIMIENTO":
        return resultado
    else:
      
        edad = resultado['listaAni'][0]['nuEdad']
        print(edad)
        if edad < 18:
            
            return dnivir_menores(dni)
        else:
                datos = resultado['listaAni'][0]

                url2 = "https://ubis-gustavxrossi.replit.app/consulta?distrito="+ datos["distrito"]
                
                response = requests.get(url2)
                resultado2 = response.json()

                apellido_paterno = datos["apePaterno"]
                apellido_paterno2 = datos["apePaterno"] + '<<' + datos["preNombres"].replace(" ", "<",)
                apellido_materno = datos['apeMaterno']
                nombres = datos['preNombres']
                dni = datos['nuDni']
                sexo = datos['sexo'][0]
                dni1 = dni + '<' + str(random.randint(0, 9))
                caducidad = datos["feCaducidad"].replace("/", " ")
                emision = datos["feEmision"].replace("/", " ")
                digitoverfi = datos["digitoVerificacion"]
                inscripcion = datos["feInscripcion"].replace("/", " ")
                fenacimiento = datos["feNacimiento"].replace("/", " ")
                fenacimiento2 = datos["feNacimiento"][8]+datos["feNacimiento"][9]+datos["feNacimiento"][3]+datos["feNacimiento"][4]+datos["feNacimiento"][0]+datos["feNacimiento"][1]+ str(random.randint(0, 9))+datos["sexo"][0]+datos["feCaducidad"][8]+datos["feCaducidad"][9]+datos["feCaducidad"][3]+datos["feCaducidad"][4]+datos["feCaducidad"][0]+datos["feCaducidad"][1]+ str(random.randint(0, 9))+ "PER"
                civil = datos["estadoCivil"][0]
                
                foto = resultado['foto']
                firma = resultado['firma']
                hderecha = resultado['hderecha']

                ubigeo_nac = resultado2["ubigeo"]
                dona_organos = datos["donaOrganos"]

                foto_without_newline = foto.replace("\n", "")
                image_data = base64.b64decode(foto_without_newline)
                image_buffer1 = BytesIO(image_data)
                foto_image = Image.open(image_buffer1)

                firma_without_newline = firma.replace("\n", "")
                image_data = base64.b64decode(firma_without_newline)
                image_buffer3 = BytesIO(image_data)
                firma_image = Image.open(image_buffer3)

                hderecha_without_newline = hderecha.replace("\n", "")
                image_data = base64.b64decode(hderecha_without_newline)
                image_buffer2 = BytesIO(image_data)
                huella_image = Image.open(image_buffer2)

                departamente = datos["depaDireccion"]

                provincia = datos['provincia']

                distrito = datos["distDireccion"]

                direccion = datos["desDireccion"]

                PLANTILLA = Image.open("./Templates/Blue/FRONTAL.jpg")
                resized_image = foto_image.resize((410, 580))
                PLANTILLA.paste(resized_image, (105, 210))

                LETRA = Image.open("./Templates/LETRAFONDO.png")
                if LETRA.mode != "RGBA" and LETRA.mode != "LA":
                        LETRA = LETRA.convert("RGBA")

                dibujo = ImageDraw.Draw(LETRA)
                texto = dni
                fuente = ImageFont.truetype("./Fonts/Helveticabold.ttf", size=60)

                bbox = fuente.getbbox(texto)
                ancho_total = bbox[2] - bbox[0] + 25 * (len(texto) - 1)
                alto_total = bbox[3] - bbox[1]

                caja_texto = Image.new('RGBA', (ancho_total, alto_total), (255, 255, 255, 0))
                dibujo_texto = ImageDraw.Draw(caja_texto)

                pos_x = 0
                for letra in texto:
                                bbox = dibujo_texto.textbbox((pos_x, -5), letra, font=fuente)
                                ancho_letra = bbox[2] - bbox[0]
                                dibujo_texto.text((pos_x, -5), letra, font=fuente, fill=(156, 13, 13))
                                pos_x += ancho_letra + 25

                texto_rotado = caja_texto.rotate(270, expand=True)
                LETRA.paste(texto_rotado, (0, 0), texto_rotado)

                letra_buffer = BytesIO()
                LETRA.save(letra_buffer, format="PNG")
                letra_buffer.seek(0)
                
                draw = ImageDraw.Draw(PLANTILLA)

                font = ImageFont.truetype("./Fonts/Helveticabold.ttf", 40)
                font1 = ImageFont.truetype("./Fonts/Helveticabold.ttf", 40)
                font2 = ImageFont.truetype("./Fonts/Helveticabold.ttf", 40)
                font3 = ImageFont.truetype("./Fonts/Helveticabold.ttf", 60)
                font4 = ImageFont.truetype("./Fonts/OCR.ttf", 105)

                draw.text((220, 773), apellido_paterno.upper(), font=font, fill=(156, 13, 13))
                draw.text((530, 250), apellido_paterno.upper(), font=font1, fill=(0, 0, 0))
                draw.text((530, 390), apellido_materno.upper(), font=font1, fill=(0, 0, 0))
                draw.text((530, 530), nombres.upper(), font=font1, fill=(0, 0, 0))
                draw.text((535, 670), fenacimiento.upper(), font=font2, fill=(0, 0, 0))
                draw.text((850, 670), ubigeo_nac.upper(), font=font2, fill=(0, 0, 0))
                draw.text((535, 760), sexo.upper(), font=font2, fill=(0, 0, 0))
                draw.text((740, 762), civil.upper(), font=font2, fill=(0, 0, 0))
                draw.text((1660, 260), inscripcion.upper(), font=font1, fill=(0, 0, 0))
                draw.text((1660, 380), emision.upper(), font=font1, fill=(0, 0, 0))
                if caducidad == "DNI NO CADUCA": 
                        x_pos = 1625 
                        font = ImageFont.truetype("./Fonts/Helveticabold.ttf", size=35) 
                else: 
                        x_pos = 1660 
                font = ImageFont.truetype("./Fonts/Helveticabold.ttf", size=40) 
                draw.text((x_pos, 500), caducidad.upper(), font=font, fill=(156, 13, 13))
                draw.text((1550, 130), dni.upper(), font=font3, fill=(156, 13, 13))
                draw.text((1820, 130), "-" , font=font3, fill=(0, 0, 0))
                draw.text((1840, 130), digitoverfi.upper() , font=font3, fill=(0, 0, 0))
                draw.text((110, 900), "I<PER", font=font4, fill=(0, 0, 0))
                draw.text((1820, 1000), str(random.randint(0, 9)), font=font4, fill=(0, 0, 0))

                dni_sin=dni.replace(" ", "")

                texto = dni_sin+"<"+ str(random.randint(0, 9)).upper()
                max_letras = 23

                if len(texto) > max_letras:
                                texto_limitado = texto[:max_letras]
                else:
                                texto_limitado = texto.ljust(max_letras, "<")

                font4 = ImageFont.truetype("./Fonts/OCR.ttf", 105)
                fill = (0, 0, 0)

                draw.text((420, 900), texto_limitado, font=font4, fill=fill)

                texto = fenacimiento2.upper()
                max_letras = 27

                if len(texto) > max_letras:
                        texto_limitado = texto[:max_letras]
                else:
                        texto_limitado = texto.ljust(max_letras, "<")

                font4 = ImageFont.truetype("./Fonts/OCR.ttf", 105)
                fill = (0, 0, 0)


                draw.text((110, 1000), texto_limitado, font=font4, fill=fill)

                texto = apellido_paterno2.upper()
                max_letras = 28

                if len(texto) > max_letras:
                        texto_limitado = texto[:max_letras]
                else:
                        texto_limitado = texto.ljust(max_letras, "<")

                font4 = ImageFont.truetype("./Fonts/OCR.ttf", 105)
                fill = (0, 0, 0)

                draw.text((110, 1100), texto_limitado, font=font4, fill=fill)

                plantilla_buff = BytesIO()
                PLANTILLA.save(plantilla_buff, format="PNG")
                plantilla_buff.seek(0)

                src = img = cv2.imread('./Templates/RAYAS.png', cv2.IMREAD_UNCHANGED)
                if img.shape[2] == 4:
                                has_transparency = True
                else:
                                has_transparency = False
                if has_transparency:
                                b,g,r,a = cv2.split(img)
                                rgb_img = cv2.merge([b,g,r])
                width = 410
                height = 580
                resized_rgb_img = cv2.resize(rgb_img, (width, height), interpolation=cv2.INTER_AREA)
                if has_transparency:
                                resized_alpha = cv2.resize(a, (width, height), interpolation=cv2.INTER_AREA)
                if has_transparency:
                                resized_img = cv2.merge([resized_rgb_img, resized_alpha])
                else:
                        resized_img = resized_rgb_img
                success, encoded_image = cv2.imencode('.png', resized_img)

                if not success:
                        raise Exception("Error al codificar la imagen")
                raya2_buffer = BytesIO(encoded_image.tobytes())

                img = cv2.imdecode(np.frombuffer(letra_buffer.read(), np.uint8), cv2.IMREAD_UNCHANGED)
                if img.shape[2] == 4:
                                has_transparency = True
                else:
                                has_transparency = False
                if has_transparency:
                                b,g,r,a = cv2.split(img)
                                rgb_img = cv2.merge([b,g,r])
                width = 450
                height = 650
                resized_rgb_img = cv2.resize(rgb_img, (width, height), interpolation=cv2.INTER_AREA)
                if has_transparency:
                                resized_alpha = cv2.resize(a, (width, height), interpolation=cv2.INTER_AREA)
                if has_transparency:
                                resized_img = cv2.merge([resized_rgb_img, resized_alpha])
                else:
                                resized_img = resized_rgb_img
                success, letra2_image = cv2.imencode('.png', resized_img)

                letra_rotada_buffer = BytesIO(letra2_image.tobytes())
                letra_rotada_buffer.seek(0)

                gray = cv2.cvtColor(np.array(firma_image), cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
                thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

                thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGRA)
                thresh[:, :, 3] = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)[1]

                text_binarizado_buffer = BytesIO()
                Image.fromarray(thresh).save(text_binarizado_buffer, format="PNG")

                text_binarizado_buffer.seek(0)
                img = Image.open(text_binarizado_buffer)
                img = img.convert('RGBA')
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                dilated = cv2.dilate(np.array(img), kernel, iterations=1)
                dilated_image = Image.fromarray(dilated)

                img = dilated_image
                img = img.convert('RGBA')
                mask = img.split()[3]
                new_img = Image.new('RGBA', img.size, color=(0, 0, 0))
                new_img.putalpha(mask)
                firma2_buffer = BytesIO()
                new_img.save(firma2_buffer, format="PNG")

                img = foto_image

                img = img.convert('L')
                output_buffer = BytesIO()
                img.save(output_buffer, format='JPEG')
                output_buffer.seek(0)

                img = Image.open(output_buffer).convert('RGB')
                img = img.convert('L')
                output_buffer = BytesIO()
                img.save(output_buffer, format='JPEG')
                output_buffer.seek(0)
                
                img = Image.open(output_buffer).convert('RGB')
                img = img.convert('L')
                pixdata = img.load()
                for y in range(img.size[1]):
                                for x in range(img.size[0]):
                                                if pixdata[x, y] != 0:
                                                                pixel = pixdata[x, y]
                                                                pixdata[x, y] = min(255, int(pixel * 1))
                output_buffer = BytesIO()
                img.save(output_buffer, format='JPEG')
                img = img.filter(ImageFilter.SMOOTH_MORE)
                img = img.convert('RGBA')
                pixdata = img.load()
                for y in range(img.size[1]):
                        for x in range(img.size[0]):
                                if pixdata[x, y][0] > 200 and pixdata[x, y][1] > 200 and pixdata[x, y][2] > 200:
                                        pixdata[x, y] = (255, 255, 255, 0)
                                elif pixdata[x, y][0] > 180 and pixdata[x, y][1] > 180 and pixdata[x, y][2] > 180:
                                        pixdata[x, y] = (215, 215, 215, 0)
                imagen_sin_fondo2_buffer = BytesIO()
                img.save(imagen_sin_fondo2_buffer, format="PNG")
                imagen_sin_fondo2_buffer.seek(0)

                img = Image.open(imagen_sin_fondo2_buffer)

                enhancer = ImageEnhance.Contrast(img)
                img_con_contraste = enhancer.enhance(3.5)

                img_con_contraste_buffer = BytesIO()
                img_con_contraste.save(img_con_contraste_buffer, format='PNG')
                img_con_contraste_buffer.seek(0)

                img = Image.open(img_con_contraste_buffer)

                transparency = Image.new('RGBA', img.size, (0, 0, 0, 0))
                alpha = 0.4
                result = Image.blend(img, transparency, alpha)

                result_buffer = BytesIO()
                result.save(result_buffer, format='PNG')
                result_buffer.seek(0)

                img23 = Image.open(result_buffer)

                size = (150, 200)
                img_resized = img23.resize(size)

                img_resized_buffer = BytesIO()
                img_resized.save(img_resized_buffer, format='PNG')
                img_resized_buffer.seek(0)

                from rembg import remove
                from PIL import Image

                output_buffer.seek(0)

                img = Image.open(output_buffer)
                img = remove(img)

                imagen_con_filtro_buffer = BytesIO()
                img.save(imagen_con_filtro_buffer, format="PNG")
                imagen_con_filtro_buffer.seek(0)
                img = Image.open(imagen_con_filtro_buffer)           

                img = img.convert('RGBA')

                filtro = Image.new('RGBA', img.size, (40, 85, 98, int(96*1.3)))

                img_con_filtro = Image.alpha_composite(img, filtro)

                img_con_filtro.putalpha(img.split()[3])

                imagen_con_filtro_buffer = BytesIO()
                img_con_filtro.save(imagen_con_filtro_buffer, format='PNG')
                imagen_con_filtro_buffer.seek(0)

                img = Image.open(imagen_con_filtro_buffer)

                enhancer = ImageEnhance.Contrast(img)
                img_con_contraste = enhancer.enhance(3.5)

                foto_mini_buffer = BytesIO()
                img_con_contraste.save(foto_mini_buffer, format='PNG')
                foto_mini_buffer.seek(0)

                img = Image.open(foto_mini_buffer)

                transparency = Image.new('RGBA', img.size, (0, 0, 0, 0))
                alpha = 0.5
                result = Image.blend(img, transparency, alpha)

                foto_mini_buffer = BytesIO()
                result.save(foto_mini_buffer, format='PNG')
                foto_mini_buffer.seek(0)

                img23 = Image.open(foto_mini_buffer)

                size = (150, 200)
                img_resized = img23.resize(size)

                foto_mini_buffer = BytesIO()
                img_resized.save(foto_mini_buffer, format='PNG')
                foto_mini_buffer.seek(0)

                img23 = Image.open(firma2_buffer)

                size = (400, 180)
                img_resized = img23.resize(size)
                output_buffer_resized = BytesIO()
                img_resized.save(output_buffer_resized, format="PNG")


                imagen_jpg = Image.open(plantilla_buff)
                imagen_png = Image.open(output_buffer_resized) 
                imagen_mini = Image.open(foto_mini_buffer)
                imagen_lineas = Image.open(raya2_buffer)

                imagen_texto = Image.open(letra_rotada_buffer)
                imagen_mini2 = Image.open(img_resized_buffer)

                dni_frontal = Image.new('RGB', imagen_jpg.size, (255, 255, 255))
                dni_frontal.paste(imagen_jpg, (0, 0))
                dni_frontal.paste(imagen_png, (1150, 650), imagen_png)
                dni_frontal.paste(imagen_mini2, (1710, 640), imagen_mini2)
                dni_frontal.paste(imagen_mini, (1710, 640), imagen_mini)
                dni_frontal.paste(imagen_lineas, (105, 210), imagen_lineas)
                dni_frontal.paste(imagen_texto, (80, 240), imagen_texto)

                from PIL import Image, ImageDraw, ImageFont

                REVERSO= Image.open(f'./Templates/Blue/POSTERIOR.jpg')

                background = Image.open(f'./Templates/Blue/POSTERIOR.jpg')

                new_size = (310, 420)
                resized_image = huella_image.resize(new_size)

                background.paste(resized_image, (1550, 43))

                draw = ImageDraw.Draw(background)
                font1 = ImageFont.truetype("./Fonts/Helveticabold.ttf", 40)
                font2 = ImageFont.truetype("./Fonts/Helveticabold.ttf", 50)

                draw.text((90, 550), departamente.upper(), font=font1, fill=(48, 47, 47))
                draw.text((510, 550), provincia.upper(), font=font1, fill=(48, 47, 47))
                draw.text((1090, 550), distrito.upper(), font=font1, fill=(48, 47, 47))
                draw.text((90, 670), direccion.upper(), font=font1, fill=(48, 47, 47))
                draw.text((513, 813), dona_organos.upper(), font=font2, fill=(48, 47, 47))
                draw.text((1350, 813), ubigeo_nac.upper() , font=font2, fill=(48, 47, 47))

                frontal_buffer = BytesIO()
                posterior_buffer = BytesIO()

                dni_frontal.save(frontal_buffer, format='JPEG')
                background.save(posterior_buffer, format='JPEG')

                frontal_base64 = base64.b64encode(frontal_buffer.getvalue()).decode('utf-8')
                posterior_base64 = base64.b64encode(posterior_buffer.getvalue()).decode('utf-8')

                frontal_buffer.seek(0)
                posterior_buffer.seek(0)

                return {'posterior_base64': frontal_base64, 'frontal_base64': posterior_base64, 'datos': resultado["listaAni"]}

if __name__ == '__main__':
    pass