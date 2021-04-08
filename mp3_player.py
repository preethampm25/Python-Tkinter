from tkinter import *
from tkinter import filedialog, ttk
import pygame
import time
from mutagen.mp3 import MP3

root = Tk()
root.title('Music Player')
root.geometry('500x400')
root.iconbitmap('icons/music.ico')
root.resizable(width=False, height=False)

# Initializing py-game
pygame.mixer.init()


# Function deals with time
def play_time():
    # Check to see if song is stop
    if stopped:
        song_slider.config(value=0)
        return

    current_time = pygame.mixer.music.get_pos() / 1000  # 1000 because it converts milli-sec to sec

    # Converting song time to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # Reconstruct song with directory
    song = playlist_box.get(ACTIVE)
    song = f'F:/mp3/{song}.mp3'

    # Find Current Song Length
    song_mut = MP3(song)

    # Total length of a song
    global song_length
    song_length = song_mut.info.length
    # Convert to time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # Check to see the song is over
    if int(song_slider.get()) == int(song_length):
        stop()

    elif paused:
        # Check to see if paused, if so - pass
        pass

    else:
        # Move slider along 1 second at a time
        next_time = int(song_slider.get()) + 1

        # Output new time value to slider, and to length
        song_slider.config(to=song_length, value=next_time)

        # Convert Slider position to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

        # Output slider
        status_bar.config(text=f"{converted_current_time} / {converted_song_length}  ")

    # Adding current time and Total song time to status bar
    if current_time >= 1:
        status_bar.config(text=f"{converted_current_time} / {converted_song_length}  ")

    # Check the loop every second

    status_bar.after(1000, play_time)


# Adding One songs
def add_song():
    song = filedialog.askopenfilename(initialdir='F:/mp3/', title='Choose a song',
                                      filetypes=(('mp3 files', '*.mp3'), ('m4a files', '*.m4a'),))
    # Strip out directory and file extention
    song = song.replace('F:/mp3/', "")
    song = song.replace('.mp3', "")
    song = song.replace('.m4a', "")

    playlist_box.insert(END, song)


# Add many songs
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='F:/mp3/', title='Choose a song',
                                        filetypes=(('mp3 files', '*.mp3'), ('m4a files', '*.m4a'),))
    # Strip out directory and file extention
    for song in songs:
        song = song.replace('F:/mp3/', "")
        song = song.replace('.mp3', "")
        # song = song.replace('.m4a', "")
        playlist_box.insert(END, song)


# Function remove from playlist
def remove_song():
    playlist_box.delete(ANCHOR)


# Function to remove all songs from playlist
def remove_all_songs():
    playlist_box.delete(0, END)


# Play function
def play():
    # Set Stopped to false
    global stopped
    stopped = False

    # Reconstruct song with directory
    song = playlist_box.get(ACTIVE)
    song = f'F:/mp3/{song}.mp3'

    # Load song to pygame mixer
    pygame.mixer.music.load(song)
    # Play song to pygame mixer
    pygame.mixer.music.play(loops=0)

    # Get song Time
    play_time()


# Create Stopped Variable
global stopped
stopped = False


# Stop Function
def stop():
    # Stop song
    pygame.mixer.music.stop()

    # Clear Playlist Bar
    playlist_box.selection_clear(ACTIVE)

    # Status Bar update when it is stopped
    status_bar.config(text="00:00/ 00:00 ")

    # Set stop variable to True
    global stopped
    stopped = True


# Creating paused variable
global paused
paused = False


# Pause Function
def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        # Un-pause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True


# Next Song Function
def next_song():
    # Reset status and Slider position to zero
    status_bar.config(text="00:00 / 00:00  ")
    song_slider.config(value=0)

    next_one = playlist_box.curselection()
    next_one = next_one[0] + 1

    # Get song name from playlist
    song = playlist_box.get(next_one)
    # Add song structure
    song = f'F:/mp3/{song}.mp3'

    # Load song to py-game mixer
    pygame.mixer.music.load(song)
    # Play song to py-game mixer
    pygame.mixer.music.play(loops=0)

    # Clear Active Bar in Playlist
    playlist_box.selection_clear(0, END)

    # Move active bar to next song
    playlist_box.activate(next_one)

    # Set active bar to next song
    playlist_box.selection_set(next_one, last=None)


# Previous Song Function
def previous_song():
    # Reset status and Slider position to zero
    status_bar.config(text="00:00 / 00:00  ")
    song_slider.config(value=0)

    next_one = playlist_box.curselection()
    next_one = next_one[0] - 1

    # Get song name from playlist
    song = playlist_box.get(next_one)
    # Add song structure
    song = f'F:/mp3/{song}.mp3'

    # Load song to py-game mixer
    pygame.mixer.music.load(song)
    # Play song to py-game mixer
    pygame.mixer.music.play(loops=0)

    # Clear Active Bar in Playlist
    playlist_box.selection_clear(0, END)

    # Move active bar to next song
    playlist_box.activate(next_one)

    # Set active bar to next song
    playlist_box.selection_set(next_one, last=None)


# Song Slider
def song_slide(x):
    # Reconstruct song with directory
    song = playlist_box.get(ACTIVE)
    song = f'F:/mp3/{song}.mp3'

    # Load song to py-game mixer
    pygame.mixer.music.load(song)
    # Play song to py-game mixer
    pygame.mixer.music.play(loops=0, start=song_slider.get())


# Create Volume Function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())


#  Create Main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

# Create Playlist Box
playlist_box = Listbox(main_frame, bg='black', fg='green', width=60, selectbackground='green')
playlist_box.grid(row=0, column=0)

# Volume slider Frame
volume_frame = LabelFrame(main_frame, text='Volume', )
volume_frame.grid(row=0, column=1, padx=10, )

volume_slider = ttk.Scale(volume_frame, from_=0, to=1, value=0.70, orient=VERTICAL, length=125, command=volume)
volume_slider.pack(pady=10, )

# Song Slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, value=0, orient=HORIZONTAL, length=360, command=song_slide)
# song_slider.pack()
song_slider.grid(row=2, column=0, pady=20)

# Button Images
back_btn_img = PhotoImage(file='images/back50.png')
froward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')

# Create Buttons Frame
control_frame = Frame(main_frame, )
control_frame.grid(row=1, column=0, pady=20)

# Buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
froward_button = Button(control_frame, image=froward_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

# Packing Buttons
back_button.grid(row=0, column=0, padx=10)
froward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create Add song Menu Drop Down
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label='Add Songs', menu=add_song_menu)
add_song_menu.add_command(label='Add One Song to playlist', command=add_song)
add_song_menu.add_command(label='Add Many Song to playlist', command=add_many_song)

# Delete song
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label='Remove Songs', menu=remove_song_menu, )
remove_song_menu.add_command(label='Remove song from Playlist', command=remove_song)
remove_song_menu.add_command(label='Clear Playlist', command=remove_all_songs)

# Create Status Bar
status_bar = Label(root, text='00:00 / 00:00  ', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Temporary Label
my_label = Label(root, text='')
my_label.pack(pady=20)

root.mainloop()
