from Tkinter import *
import sys
import time
import threading

import UDPLocalSock

class App(Frame):
	def __init__(self, master, remote_sock):
		frame = Frame(master)
		frame.pack()
		
		self.scrollbar = Scrollbar(frame)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		
		self.uptext = Text(frame)
		#self.uptext.insert(INSERT, 'Insert Text')
		self.uptext.place(relx = 0.5,rely = 0.3,anchor = CENTER)
		self.uptext['yscrollcommand'] = self.scrollbar.set
		self.scrollbar['command'] = self.uptext.yview
		self.uptext.bind('<Key>', self.recvfrom_sock_inwindow)
		self.uptext.pack(side=TOP)
		
		self.quit = Button(frame, text='Quit', command=frame.quit)
		self.quit.place(relx = 0.2,rely = 1.0,anchor = CENTER) 
		self.quit.pack(side=BOTTOM)
		
		self.send = Button(frame, text='Send', command=self.send_message)
		self.send.place(relx = 0.8,rely = 1.0,anchor = CENTER) 
		self.send.pack(side=BOTTOM)
		
		self.downtext = Text(frame)
		self.downtext.place(relx = 0.5,rely = 0.8,anchor = CENTER)
		self.downtext.pack(side=BOTTOM)
	
	def send_message(self):
		print 'Send message'
		message = self.downtext.get(1.0,END)
		if (message == '\n'):
			print 'Can\'t send empty msg.'
			return
		self.downtext.delete(1.0,END)
		self.uptext.insert(END, 'I say: ' + message)
		
		#UDPLocalSock.send_message(self.local_sock, self.remote_sock, message)
		# send message to remote addr
		sendto_sock(message)
		
	def print_message(self, message):
		#print 'Print message'
		self.uptext.insert(END, message)
		
	def recvfrom_sock_inwindow(self):
		#self.print_message('Begin to receive message.')
		while True:
			#self.print_message('Receive 1.')
			next_line = sys.stdin.readline()
			sys.stdin.flush()
			#self.print_message('Receive 2.')
			if next_line:
				self.print_message(next_line)
				next_line = None

def recvfrom_sock(app):
	print 'Window begins to recv message.'
	next_line = None
	while True:
		next_line = sys.stdin.readline()
		sys.stdin.flush()
		if next_line:
			app.print_message(next_line)
			next_line = None
		else:
			time.sleep(0.5)
		
def sendto_sock(message):
	sys.stdout.write(message)
	sys.stdout.flush()

def create_window(remote_sock):
	root = Tk()
	root.wm_title('Talking to ' + '9991')
	root.geometry('500x500+0+0')
	app = App(root, remote_sock)
	
	recv_thread = threading.Thread(name='Recving', target=app.recvfrom_sock_inwindow, args=())
	recv_thread.start()
	
	#-------------------------------------------------------------------------------------------------------------
	#TRY TO recv message directly by uptext
	#-------------------------------------------------------------------------------------------------------------
	
	root.mainloop()

	'''
	recv_thread = threading.Thread(name='Recving', target=recvfrom_sock, args=(app,))
	recv_thread.start()
	
	time.sleep(1)
	
	while True:
		if recv_thread.is_alive():
			print 'Alive'
			root.mainloop()
			break
		else:
			print 'Dead'
			time.sleep(0.3)
			'''
		
if __name__ == '__main__':
	create_window(sys.argv[1])
	