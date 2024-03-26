from spleeter.separator import Separator

def main():
    # Create a separator with the 2stems configuration
    separator = Separator('spleeter:2stems')

    # Use the separator to separate the audio
    separator.separate_to_file('audiofile1.mp3', 'output')

    print("Audio separation completed. Check the 'output' directory for the separated audio tracks.")

if __name__ == '__main__':
    main()