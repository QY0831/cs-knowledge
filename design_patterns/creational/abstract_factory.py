"""
抽象工厂模式：
为创建对象提供接口，代替指定具体的类。
通过特定的工厂，传入需要的对象信息，工厂即可返回创建的对象。

例子：
当我们需要Dog或Cat时，我们调用对应宠物工厂的buy_pet()方法来得到Pet对象。
"""
class Pet:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


class Dog(Pet):
    def speak(self) -> None:
        print("woof")

    def __str__(self) -> str:
        return f"Dog<{self.name}>"


class Cat(Pet):
    def speak(self) -> None:
        print("meow")

    def __str__(self) -> str:
        return f"Cat<{self.name}>"


class PetShop:

    """A pet shop"""

    def __init__(self, animal_factory: Type[Pet]) -> None:
        """pet_factory is our abstract factory.  We can set it at will."""

        self.pet_factory = animal_factory

    def buy_pet(self, name: str) -> Pet:
        """Creates and shows a pet using the abstract factory"""

        pet = self.pet_factory(name)
        print(f"Here is your lovely {pet}")
        return pet


# Show pets with various factories
def main() -> None:
    """
    # A Shop that sells only cats
    >>> cat_shop = PetShop(Cat)
    >>> pet = cat_shop.buy_pet("Lucy")
    Here is your lovely Cat<Lucy>
    >>> pet.speak()
    meow

    # A shop that sells random animals
    >>> shop = PetShop(random_animal)
    >>> for name in ["Max", "Jack", "Buddy"]:
    ...    pet = shop.buy_pet(name)
    ...    pet.speak()
    ...    print("=" * 20)
    Here is your lovely Cat<Max>
    meow
    ====================
    Here is your lovely Dog<Jack>
    woof
    ====================
    Here is your lovely Dog<Buddy>
    woof
    ====================
    """