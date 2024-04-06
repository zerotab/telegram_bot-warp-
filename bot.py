# IMPORTAMOS TODO LO DEL ARCHIVO DE CONFIGURACIÓN
from config import *

# INSTANCIAMOS EL BOT DE TELEGRAM
bot = telebot.TeleBot(TOKEN)




####################################################################################
####################### FUNCION PARA GENERAR LOS GB DE WARP+ #######################
####################################################################################
def generar(message, gigas, id, cliente):
	referrer = id
	def genString(stringLength):
		try:
			letters = string.ascii_letters + string.digits
			return ''.join(random.choice(letters) for i in range(stringLength))
		except Exception as error:
			print(error)		    
	def digitString(stringLength):
		try:
			digit = string.digits
			return ''.join((random.choice(digit) for i in range(stringLength)))    
		except Exception as error:
			print(error)	
	url = f'https://api.cloudflareclient.com/v0a{digitString(3)}/reg'
	def run():
		try:
			install_id = genString(22)
			body = {"key": "{}=".format(genString(43)),
					"install_id": install_id,
					"fcm_token": "{}:APA91b{}".format(install_id, genString(134)),
					"referrer": referrer,
					"warp_enabled": False,
					"tos": datetime.datetime.now().isoformat()[:-3] + "+02:00",
					"type": "Android",
					"locale": "es_ES"}
			data = json.dumps(body).encode('utf8')
			headers = {'Content-Type': 'application/json; charset=UTF-8',
						'Host': 'api.cloudflareclient.com',
						'Connection': 'Keep-Alive',
						'Accept-Encoding': 'gzip',
						'User-Agent': 'okhttp/3.12.1'
						}
			req         = urllib.request.Request(url, data, headers)
			response    = urllib.request.urlopen(req)
			status_code = response.getcode()	
			return status_code
		except Exception as error:
			print(error)	

	g = 0
	b = 0
	while True:
		if g == gigas:
			bot.send_message(message.chat.id, "<b>❕Recarga realizada completamente.</b>", parse_mode="html")
			bot.send_message(cliente, "<b>❕Su compra se ha sido realizada correctamente. Si tiene algún problema no dude en contactar con algún administrador, sin más que decir espero volver a interactuar con usted pronto.</b>", parse_mode="html")
			break
		else:
			result = run()
			if result == 200:
				g = g + 1
				bot.send_message(message.chat.id, f"[ - ] TRABAJANDO EN EL ID: {referrer}\n[ :) ] {g} GB han sido añadidas correctamente a la cuenta.\n[ # ] Total: {g} Bien {b} Mal\n[ # ] Faltan {gigas - g}GB para completar la recarga.\n[ * ] Después de 5 segundos se enviará una nueva petición.")
				time.sleep(5)
			else:
				b = b + 1
				os.system('cls' if os.name == 'nt' else 'clear')
				bot.send_message(message.chat.id, f"[ :( ] Error al conectar con el servidor.\n[ # ] Total: {g} Bien {b} Mal")




# Responde al comando /start
@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.reply_to(message, "<b>👋 Bienvenido, con este bot podrá comprar GB para WARP+, para ver los planes disponibles utilice el comando <code>/planes</code> y si necesita ayuda utilice el comando <code>/help</code> o <code>/ayuda</code>.</b>", parse_mode="html")


# Responde a los comandos /help y /ayuda 
@bot.message_handler(commands=["help", "ayuda"])
def cmd_help(message):
    bot.reply_to(message, "<b>❔AQUÍ TIENES COMO UTILIZAR CORRECTAMENTE EL BOT ❔\n\n➖ Si deseas comprar algún plan primero revíselos con el comando <code>/planes</code>\n➖ Luego de decidir que plan deseas comprar utiliza el siguiente comando para realizar la compra:\n〰️ <code>/comprar ID NUMERO PLAN</code>\n➖ El comando debe de introducirlo exactamente en ese orden, primero pones tu ID de WARP (si no sabes donde encontrarlo utiliza el comando <code>/id</code>) luego pones tu número telefónico y por último el número del plan que deseas comprar. Ejemplo de uso del comando <code>/comprar</code>:\n〰️ <code>/comprar  08b42c5b-62dd-491d-8da3-0c7deecbc528 56626768 3</code>\n➖ Este comando lo que hace es ordenarte una compra del plan número 3 que contiene 10GB. Recuerda que debes de transferirle el coste del plan que deseas comprar al número <code>56626768</code>.</b>", parse_mode="html")


# Responde al comando /planes
@bot.message_handler(commands=["planes"])
def cmd_planes(message):
    bot.reply_to(message, "<b>⚜️AQUÍ TIENES LOS PLANES DISPONIBLES⚜️\n1️⃣➖ 1GB x 15CUP\n2️⃣➖ 5GB x 50CUP\n3️⃣➖ 10GB x 85CUP\n4️⃣➖ 20GB x 150CUP\n5️⃣➖ 50GB x 300CUP\n6️⃣➖ 100GB x 500CUP\n\n❕Para realizar la compra de algún plan utilice el comando <code>/comprar</code>, <code>/c</code> o <code>/buy</code></b>", parse_mode="html")


# Responde al comando /setadmin o /sa
@bot.message_handler(commands=["setadmin", "sa"])
def cmd_setadmin(message):
    texto = message.text.split(" ")                             # DIVIDE EL MENSAJE CADA VEZ QUE ENCUENTRE UN ESPACIO
    admin_id = int(texto[1])                                    # DEFINE EL ADMIN_ID COMO EL SEGUNDO ELEMENTO DEL TEXTO
    for admin in ADMINISTRADORES:                               # RECORRE EL ARRAY DE LOS ADMINISTRADORES
        if message.chat.id == admin:                            # VERIFICA SI EL COMANDO LO EJECUTÓ UN ADMINISTRADOS
            if existe(ADMINISTRADORES, admin_id):               # VERIFICA SI EL ADMINISTRADOR YA EXISTE
                bot.send_message(message.chat.id, f"<b>❗️El administrador con el ID <code>{admin_id}</code> ya existe</b>", parse_mode="html")
            else:                       # SI EL ADMINISTRADO NO EXISTE ENTONCES:
                ADMINISTRADORES.append(admin_id)                                # AGREGA AL NUEVO ADMINISTRADOR AL ARRAY ADMINISTRADORES
                with open("admins.py", "w") as file:                            # ABRE EL ARCHIVO admins.py EN MODO DE ESCRITURA
                    file.write(f"ADMINISTRADORES = {ADMINISTRADORES}")          # GUARDA AL ARCHIVO CON UN ARRAY QUE CONTIENE EL ARRRAY ADMINISTRADORES CON EL NUEVO ADMINISTRADOR AGREGADO
                bot.send_message(message.chat.id, f"<b>❗️Se ha agregado correctamente el administrador con el ID <code>{admin_id}</code>\n❕Para eliminar a un administrador utilice el comando <code>/removeadmin</code> o <code>/ra</code></b>", parse_mode="html")
        else:   # SI EL ID NO ES DE UN ADMINISTRADOR ENTONCES:
            continue    # CONTINUA AL SIGUIENTE ELEMENTO DEL ARRAY
        

# Responde al comando /comprar /buy /c 
@bot.message_handler(commands=["comprar", "c", "buy"])
def cmd_buy(message):
    texto = message.text.split(" ")
    warp_id = texto[1]
    number = texto[2]
    plan = texto[3]
    for admin in ADMINISTRADORES:
        bot.send_message(admin, f"""<b>‼️HAN SOLICITADO UNA RECARGA‼️
🆔: <code>{warp_id}</code>
✈️: <code>{message.chat.id}</code>
#️⃣: <code>{number}</code>
📑: <code>{plan}</code> ({planes[plan]})
                         
🆔 ID WARP | ✈️ ID TG | #️⃣ NÚMERO | 📑 PLAN</b>
[ # ] Comando para realizar esta recarga:
<code>/recargar {warp_id} {plan} {message.chat.id}</code>""", parse_mode="html")
    bot.reply_to(message, "<b>❕Su oferta ha sido enviada a los administradores de forma correcta.\n❔Para completar su oferta envíe el costo del plan elegido al siguiente número <code>56626768</code> y un administrador le pondrá las GB en el menor tiempo posible.</b>", parse_mode="html")
    

# Responde al comando /recargar  /r
@bot.message_handler(commands=["recargar", "r"])
def cmd_recargar(message):
    texto = message.text.split(" ")
    warp_id = texto[1]
    plan = planes[int(texto[2])]
    cliente = texto[3]
    for admin in ADMINISTRADORES:
        if message.chat.id == admin:
            bot.send_message(message.chat.id, f"<b>‼️Usted está recargando el ID <code>{warp_id}</code> con {plan}GB.</b>",  parse_mode="html")
            generar(message, plan, warp_id, cliente)
        else:
            continue




######################################################################################
######################################## MAIN ########################################
######################################################################################
if __name__ == '__main__':
    print('     ███╗  ██╗██╗  ██╗      ███████╗███████╗██████╗  █████╗ \n'
'     ████╗ ██║██║ ██╔╝      ╚════██║██╔════╝██╔══██╗██╔══██╗\n'
'     ██╔██╗██║█████═╝ █████╗  ███╔═╝█████╗  ██████╔╝██║  ██║\n'
'     ██║╚████║██╔═██╗ ╚════╝██╔══╝  ██╔══╝  ██╔══██╗██║  ██║\n'
'     ██║ ╚███║██║ ╚██╗      ███████╗███████╗██║  ██║╚█████╔╝\n'
'     ╚═╝  ╚══╝╚═╝  ╚═╝      ╚══════╝╚══════╝╚═╝  ╚═╝ ╚════╝ \n')
    print ("[+] BOT PARA LA VENTA DE GB DE WARP+:")
    print ("[-] Este bot sirve para la venta de GB de WARP+.")
    print ("[-] Versión: 0.1")
    bot.infinity_polling()
    print("BOT FINALIZADO")