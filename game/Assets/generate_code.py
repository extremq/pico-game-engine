# FUN FACT: these comments are generated by chatGPT

def declare_sprite_extern(name: str, size: tuple) -> str:
    # Use string formatting to generate strings declaring extern variables
    # The extern keyword indicates that the variables are defined in another source file
    # The size tuple contains the width and height of the sprite in pixels
    pixel_array_declaration = f"\textern uint16_t const {name} [{size[0]} * {size[1]}];\n"
    alpha_array_declaration = f"\textern bool const {name}_alpha [{size[0]} * {size[1]}];\n"
    width_declaration = f"\textern uint16_t const {name}_w;\n"
    height_declaration = f"\textern uint16_t const {name}_h;\n"

    # Return the declarations as a single string
    return pixel_array_declaration + alpha_array_declaration + width_declaration + height_declaration


def write_sprite_array(name: str, pixels: list, size: tuple) -> str:
    # Initialize the buffer code and alpha code strings with the beginning of the array definitions
    # The size tuple contains the width and height of the sprite in pixels
    buffer_code = f"\tuint16_t const {name} [{size[0]} * {size[1]}] = {{"
    alpha_code = f"\tbool const {name}_alpha [{size[0]} * {size[1]}] = {{"

    # Initialize the width and height variables
    sprite_width = f"\tuint16_t const {name}_w = {size[0]};\n"
    sprite_height = f"\tuint16_t const {name}_h = {size[1]};\n"

    # Iterate through the list of pixels
    for pixel in pixels:
        # Convert the pixel color to an RGB565 value and add it to the buffer code
        # The {0:#x} format specifier is used to convert the integer value to a hexadecimal string
        buffer_code += f" {rgb888_to_rgb565(pixel[0], pixel[1], pixel[2]):#x},"

        # If the alpha value of the pixel is not zero, add "true" to the alpha code, otherwise add "false"
        alpha_code += f" {'true' if pixel[3] != 0 else 'false'},"

    # Remove the last comma from the buffer code and alpha code and add the closing brace and newline character
    buffer_code = buffer_code[:-1] + " };\n"
    alpha_code = alpha_code[:-1] + " };\n"

    # Return the buffer code, alpha code, width, and height as a single string
    return buffer_code + alpha_code + sprite_width + sprite_height


def declare_map_extern(name: str) -> str:
    # Use string formatting to generate a string declaring an extern variable
    # The extern keyword indicates that the variable is defined in another source file
    extern_declaration = f"\textern Tile const {name}[12 * 12];\n"

    return extern_declaration


def write_map_array(name: str, pixels: list) -> str:
    # Initialize the buffer code string with the beginning of the array definition
    buffer_code = f"\tTile const {name}[12 * 12] = {{"

    # Iterate through the list of pixels
    for pixel in pixels:
        # Convert the pixel color to a hexadecimal string
        hex_code = rgb888_to_hex(pixel[0], pixel[1], pixel[2])

        # Check the hex code of the pixel and add the corresponding map element to the buffer code
        # If the hex code does not match any of the predefined cases, print a warning and default to an EMPTY tile
        match hex_code:
            # TODO add prize tile
            case "#FFFFFF":
                buffer_code += " EMPTY,"
            case "#000000":
                buffer_code += " WALL,"
            case "#ED1C24":
                buffer_code += " ENEMY,"
            case "#FFF200":
                buffer_code += " PORTAL,"
            case "#5487FF":
                buffer_code += " PLAYER,"
            case "#B97A57":
                buffer_code += " BOX,"
            case _:
                print("\t\t- Warning! Invalid pixel, defaulting to EMPTY tile.")
                buffer_code += " EMPTY,"

    # Remove the last comma from the buffer code and add the closing brace and newline character
    buffer_code = buffer_code[:-1] + "};\n"

    return buffer_code


def rgb888_to_rgb565(r: int, g: int, b: int) -> int:
    # Shift the bits of the red value right by 3 places, then left by 11 places
    # Shift the bits of the green value right by 2 places, then left by 5 places
    # Shift the bits of the blue value right by 3 places
    # Add the resulting values together to obtain the RGB565 value
    rgb565 = ((r >> 3) << 11) + ((g >> 2) << 5) + (b >> 3)

    return rgb565


def rgb888_to_hex(r: int, g: int, b: int) -> str:
    # Use string formatting to create a hexadecimal string representation of the color
    # The :02x format specifier indicates that the value should be formatted as a hexadecimal string
    # The 02 specifies that the string should always have at least two digits
    # Leading zeros will be added if necessary
    hex_string = f"#{r:02x}{g:02x}{b:02x}"

    # Return the hexadecimal string in uppercase
    return hex_string.upper()
