import sys
import logging

from alma.shop import Shop

if __name__ == "__main__":
    if len(sys.argv) == 1:
        speed = 1
    elif len(sys.argv) == 2:
        try:
            speed = int(sys.argv[1])
            if speed < 1 or speed > 5:
                raise ValueError
        except ValueError:
            sys.exit("The parameter should be a number between a 1 and 5")
    else:
        sys.exit("The script works without parameters or just one")

    # Start the shop
    logging.basicConfig(level=logging.INFO)
    print("Creation of the shop")
    shop = Shop(speed)
    shop.run()
    print("End of the script")
