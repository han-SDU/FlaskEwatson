import threading
from threading import Event
from server import server

# Main entry point of application

def start_server():
	server.run()

def main():
	try:
		print('Application Started')

		print('Starting Temperature Sensor')

		print('Starting Pressure Sensor')

		print('Starting Humidity Sensor')

		print('Starting CO2 Sensor')

		print('Starting Flask Server')
		serverThread = threading.Thread(target=start_server, daemon=True)
		serverThread.start()

		Event().wait() 
		print('Exit with ctrl-c')
	except KeyboardInterrupt as e:
		print('Shutting down')

if __name__=="__main__":
	main()
