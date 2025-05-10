import wave
import numpy as np
with wave.open("sample-1.wav","rb") as audio:
    sample_rate=audio.getnframes()
    framerate=audio.getframerate()
    channel=audio.getnchannels()
    signal=audio.readframes(channel)
    width=audio.getsampwidth()
    signal_array=np.frombuffer(signal,dtype=np.int16)
    time_duration=sample_rate/float(framerate)
    t=np.linspace(0,time_duration,int(framerate*time_duration),endpoint=False)
    if len(signal_array.shape)>1:#checks whether the audio is mono or stereo
        #convert signal to 1D array
        signal_array=np.mean(signal_array,axis=1)
    dsp=np.abs(np.fft.fft(signal_array))
    frequencies=np.fft.fftfreq(len(dsp),d=1/sample_rate)
    #now find dominant frequecy by eleminating half of the frequency cuz they are negative for optimisation
    frequency_index=np.argmax(np.abs(frequencies[:len(frequencies)//2]))#for optimisaton
    freq=frequencies[frequency_index]
    binary=[]
    result=np.fft.ifft(dsp)
    for i in result:
        real=np.real(i)
        imag=np.imag(i)
        phase=np.arctan2(imag,real)
        amplitude=np.sqrt((real**2)+(imag)**2)
        bits=""
        bits_size=0
        if 0<=phase<np.pi/2:
          result=amplitude*np.sin((2*np.pi*freq*t)+phase) #1st Quadrant
          for res in result:
            if res>0.1:

              if bits_size<8:
                bits+='1'
                bits_size+=1
              else:
                binary.append(bits)
                bits=""
                bits_size=0

                bits+='1'
                bits_size+=1


            elif res<0.1:
              if bits_size<8:
                bits+='0'
                bits_size+=1
              else:
                binary.append(bits)
                bits=""
                bits_size=0

                bits+='0'
                bits_size+=1

        elif np.pi/2<=phase<np.pi:
          result=amplitude*np.cos((2*np.pi*freq*t)+phase)#2nd Quadrant
          for res in result:
            if res>0.1:
              if bits_size<8:
                bits+='1'
                bits_size+=1
              else:
                binary.append(bits)
                bits=""
                bits_size=0

                bits+='1'
                bits_size+=1

            elif res<0.1:
              if bits_size<8:
                bits+='0'
                bits_size+=1
              else:
                binary.append(bits)
                bits=""
                bits_size=0

                bits+='0'
                bits_size+=1

        elif np.pi<=phase<3*np.pi/2:#3rd Quadrant
          result=-amplitude*np.sin((2*np.pi*freq*t)+phase)
          for res in result:
            if res>0.1:
              if bits_size<8:
                bits+='1'
                bits_size+=1
              else:
                binary.append(bits)
                bits=""
                bits_size=0

                bits+='1'
                bits_size+=1

            elif res<0.1:
              if bits_size<8:
                bits+='0'
                bits_size+=1
              else:
                binary.append(bits)
                bits=""
                bits_size=0

              bits+='0'
              bits_size+=1

        elif 3*np.pi/2<=phase <2*np.pi:#4th Quadrant
          result=-amplitude*np.cos((2*np.pi*freq*t)+phase)
          for res in result:
            if res>0.1:
              if bits_size<8:
                bits+='1'
                bits_size+=1
              else:
                binary.append(bits)
                bits=""
                bits_size=0

                bits+='1'
                bits_size+=1

            elif res<0.1:
              if bits_size<8:
                bits+='0'
                bits_size+=1
              else:
                binary.append(bits)
                bits=""
                bits_size=0

                bits+='0'
                bits_size+=1
    print("")
    print("CALCULATION COMPLETED......")
    print()

    with open("binary.txt","w") as binary_file:
      binary_file.writelines(bits+'  ' for bits in binary)

    print("FILE SUCCESFULLY CREATED")





