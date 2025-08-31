from main import main

fn = "main"

match fn:
    case "main":
        main()
    case _:
        print("non")