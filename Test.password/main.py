import urwid

def has_digit(password):
    for character in password:
        if character.isdigit():
            return True
    return False

def has_letters(password):
    for character in password:
        if character.isalpha():
            return True
    return False

def is_very_long(password):
    if len(password) > 12:
        return True
    else:
        return False

def has_upper_letters(password):
    for character in password:
        if character.isupper():
            return True
    return False

def has_lower_letters(password):
    for character in password:
        if not character.isupper():
            return True
    return False

def has_symbols(password):
    for character in password:
        if not character.isdigit() and not character.isalpha():
            return True
    return False

def has_not_only_symbols(password):
    for character in password:
        if not has_symbols(character):
            return True
    return False

def test_password(edit, password):
    score = 0
    set_of_tests = [
        has_lower_letters,
        has_upper_letters,
        has_letters,
        has_digit,
        is_very_long,
        has_not_only_symbols,
        has_symbols,
    ]
    for test in set_of_tests:
       if test(password):
           score += 2
    native_password.set_text("Your password: %s" % password)
    total_score.set_text("Password rating: %s" % score)

if __name__ == '__main__':

    password = urwid.Edit('Enter password: ', mask='*')
    native_password = urwid.Text('')
    total_score = urwid.Text('')
    menu = urwid.Pile([password, native_password, total_score])
    urwid.connect_signal(password, 'change', test_password)
    menu = urwid.Filler(menu, valign='top')
    urwid.MainLoop(menu).run()