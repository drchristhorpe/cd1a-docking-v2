from steps import generate_conformers
import toml

config = toml.load('config.toml')

generate_conformers('7ryn', config)