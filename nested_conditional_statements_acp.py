holiday = input('Are you going on holiday? (Type yes or no) ')

if holiday == 'yes':
    dest = input('Are you going to the beach or the mountains? (Type 1 for beach and 2 for the mountains) ')

    if dest == '1':
        beach_plan = input('What are you planning to do on the beach? (Type 1 for swimming and 2 for building sandcastles) ')

        if beach_plan == '1':
            print('Enjoy your time at the beach. The best time for swimming is in the late afternoon as that is when the weather will be the warmest. Make sure to carry sunscreen!')
        elif beach_plan == '2':
            print("Enjoy your time at the beach. The best time for building sandcastles is during the day with sunlight. Bring a bucket and shovel. Make sure to build the sandcastle near the water so the sand doesn't fall off.")
        else:
            print('Invalid input given.')

    elif dest == '2':
        mount_plan = input('Are you planning to go camping or hiking? (Type 1 for camping and 2 for hiking) ')

        if mount_plan == '1':
            print('Enjoy your time in the mountains. Make sure to carry your tent and sleeping bags to sleep comfortably and warmly. It can get cold at night! You should also not wander at night as there can be dangerous creatures like bears!')
        elif mount_plan == '2':
            print('Enjoy your time in the mountains. Make sure to carry waterproof and comfortable hiking boots. Carry a jacket as it can get chilly in the mountains. Make sure to carry plenty of water to keep yourself hydrated!')
        else:
            print('Invalid input given.')

    else:
        print('Invalid input given.')

elif holiday == 'no':
    print('Enjoy your time at home!')

else:
    print('Invalid input given.')