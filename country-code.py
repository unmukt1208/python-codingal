country_code = {
    'India': '+91',
    'Germany': '+49',
    'Bangladesh': '+88',
    'Belgium': '+32',
    'America': '+1',
    'Australia': '+61',
    'Canada': '+1',
    'France': '+33',
    'Greece': '+30',
    'Italy': '+39',
    'Spain': '+34',
    'Sweden': '+46',
    'United Kingdom': '+44',
    'Japan': '+81',
    'Mexico': '+52'
}
user_country = input('Which countrys phone code do you want to find?: ')
for i in country_code:
    if i == user_country:
        print(country_code[i])
        
else:
    print('Sorry, we do not have any information on that country')