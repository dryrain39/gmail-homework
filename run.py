import sys

print sys.argv

if sys.argv[1] == 'gmail':
    import main
    main.start()
    pass

if sys.argv[1] == 'reg_service':
    pass

if sys.argv[1] == 'del_service':
    pass

