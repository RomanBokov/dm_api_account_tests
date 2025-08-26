def attempt(
        n=5
        ):

    def decorator(
            func
            ):
        def wraps(
                *args,
                **kwargs
                ):
            print('--------')
            print(n)
            func(*args, **kwargs)
            print('--------')
            return

        return wraps
    return decorator

@attempt(n=999)
def my_print1(
        name
        ):
    print(f"Hellow, {name}")


@attempt(n=1)
def my_print2(
        name
        ):
    print(f"Hellow, {name}")


@attempt()
def my_print3(
        name
        ):
    print(f"Hellow, {name}")


@attempt(n=3)
def my_print4(
        name
        ):
    print(f"Hellow, {name}")


my_print1(name='Piter')
my_print2(name='Marusia')
my_print3(name='Vlad')
my_print4(name='Roman')
