from components import Components

def loop():
    # Store city and state names and whether they were entered
    city = ""
    state = ""
    city_entered = False
    state_entered = False

    while 69 == 69:
        # Ask for city if not entered
        if city_entered is False:
            city_input = input("Enter the city name: ")

        # Ask for city if not entered
        if state_entered is False:
            state_input = input("Enter the state or territory abbreviation: ")

        # If valid city, take as input and say it was entered
        if len(city_input) > 0:
            city = str.lower(city_input)
            city_entered = True
        else:
            print("Please enter a valid city!\n")

        # If valid state abbreviation, take as input and say it was entered
        if len(state_input) == 2:
            state = str.lower(state_input)
            state_entered = True
        else:
            print("Please enter a valid 2 letter state abbreviation!\n")

        if city_entered is True and state_entered is True:
            comps = Components(city, state)
            break

if __name__ == "__main__":
    loop()