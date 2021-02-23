# No Imports Allowed!
def backwards(sound):
    """
    Takes an input .wav file and reverses the left and right audio
    """
    #Helper function that makes a copy so original file is untouched
    rate, base_left, base_right = copy(sound) 
    
    rev_left = base_left[::-1] 
    rev_right = base_right[::-1] 

    rev_sound = {'rate':rate,'left':rev_left,'right':rev_right}
    return rev_sound

def mix(sound1, sound2, p):
    """
    Takes two .wav input files and outputs a .wav file that mixes both
    sound files according to a proportional ratio, p, as a float.
    """
    rate1, base_left1, base_right1 = copy(sound1)
    rate2, base_left2, base_right2 = copy(sound2)

    if not rate1 == rate2: #checking the different sample rate case
        return None
    
    mix_left = [i*p+j*(1-p) for i,j in zip(base_left1,base_left2)]
    mix_right = [i*p+j*(1-p) for i,j in zip(base_right1,base_right2)]

    mix_sound = {'rate':rate1,'left':mix_left,'right':mix_right}
    return mix_sound

def echo(sound, num_echos, delay, scale):
    """
    Takes in a .wav file and outputs an echoed .wav file according to the
    number of echoes, the delay between echoes, and the scale factor of the echoes.
    """
    
    rate, base_left, base_right = copy(sound)
    
    sample_delay = round(delay * rate) #Number of delays as an int
    
    echo_left = [0]*len(base_left) #list of 0 so loop can add the base values
    echo_right = [0]*len(base_right)
    
    for i in range(num_echos+1):
        if i>0:
            echo_left.extend([0]*sample_delay)
            echo_right.extend([0]*sample_delay)
        #Scales the echo and adds the echo to the modified audio.    
        add_left = [0]*sample_delay*i+[value*(scale**i) for value in base_left]
        echo_left = [a + b for a, b in zip(echo_left,add_left)]

        add_right = [0]*sample_delay*i+[value*(scale**i) for value in base_right]
        echo_right = [a + b for a, b in zip(echo_right,add_right)]
        
    echo_sound = {'rate':rate,'left':echo_left,'right':echo_right}
    return echo_sound

def pan(sound):
    """
    Takes in a .wav file and outputs a .wav file where the audio pans from the left to right.
    """
    rate, base_left, base_right = copy(sound)
    
    length = len(base_left)
    pan_left = [value*(1-count/(length-1)) for count, value in enumerate(base_left)]
    pan_right = [value*(count/(length-1)) for count, value in enumerate(base_right)]

    pan_sound = {'rate':rate,'left':pan_left,'right':pan_right}
    return pan_sound

def remove_vocals(sound):
    """
    Takes in a .wav file and returns the difference between the left and right audio
    to quickly remove the vocal audio.
    """
    rate, base_left, base_right = copy(sound)
    #Computes difference
    rem_right = [a - b for a, b in zip(base_left,base_right)]
    rem_left = rem_right
    
    rem_sound = {'rate':rate,'left':rem_left,'right':rem_right}
    return rem_sound

def copy(sound):
    """
    Creates a shallow copy and removes dictionary so the original file is not touched
    """
    rate = sound['rate'] #Shallow copies
    base_left = sound['left']
    base_right = sound['right']
    return rate, base_left, base_right

# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io
import wave
import struct

def load_wav(filename):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, 'r')
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    left = []
    right = []
    for i in range(count):
        frame = f.readframes(1)
        if chan == 2:
            left.append(struct.unpack('<h', frame[:2])[0])
            right.append(struct.unpack('<h', frame[2:])[0])
        else:
            datum = struct.unpack('<h', frame)[0]
            left.append(datum)
            right.append(datum)

    left = [i/(2**15) for i in left]
    right = [i/(2**15) for i in right]

    return {'rate': sr, 'left': left, 'right': right}


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, 'w')
    outfile.setparams((2, 2, sound['rate'], 0, 'NONE', 'not compressed'))

    out = []
    for l, r in zip(sound['left'], sound['right']):
        l = int(max(-1, min(1, l)) * (2**15-1))
        r = int(max(-1, min(1, r)) * (2**15-1))
        out.append(l)
        out.append(r)

    outfile.writeframes(b''.join(struct.pack('<h', frame) for frame in out))
    outfile.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    
    #backwards
    mystery = load_wav('D:/MIT/6.009/lab0/sounds/mystery.wav')
    write_wav(backwards(mystery), 'D:/MIT/6.009/lab0/sounds/mystery_reversed.wav')
    #mix
    synth = load_wav('D:/MIT/6.009/lab0/sounds/synth.wav')
    water = load_wav('D:/MIT/6.009/lab0/sounds/water.wav')
    write_wav(mix(synth,water,0.2), 'D:/MIT/6.009/lab0/sounds/synth_water_mix.wav')
    #echo
    echos = load_wav('D:/MIT/6.009/lab0/sounds/chord.wav')
    write_wav(echo(echos,5,0.3,0.6), 'D:/MIT/6.009/lab0/sounds/chord_echo.wav')
    #pan
    car = load_wav('D:/MIT/6.009/lab0/sounds/car.wav')
    write_wav(pan(car), 'D:/MIT/6.009/lab0/sounds/pan_car.wav')
    #remove vocals
    coffee = load_wav('D:/MIT/6.009/lab0/sounds/coffee.wav')
    write_wav(remove_vocals(coffee), 'D:/MIT/6.009/lab0/sounds/rem_coffee.wav')