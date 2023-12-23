import sys
import os
import bpy

blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

import boxes
import boxes.generators

import argparse



print("")
print("----------Running Boxes Script--------------")
print("Location of Blender file :")
""" print(blend_dir)
 """
def generators_by_name():
    all_generators = boxes.generators.getAllBoxGenerators()

    return {
        name.split('.')[-1].lower(): generator
        for name, generator in all_generators.items()
    }

def parseType(type):
    if isinstance(type, boxes.BoolArg):
        t = '"bool"'
        return ("Boolean")
    #le travail pour terminer cette fonction serait de connaitre 
    #sous quelle forme doit être retournée la valeur pour l'UI de Blender



def paramGetter(param):
    """ name = param.option_strings[0].replace("-", "")
    print(name) """
    
    #on retire les params d'aide
    if isinstance(param, argparse._HelpAction):
        return None 
    
    if param.choices:
        uniqueChoices = []
        for e in param.choices:
            if e not in uniqueChoices:
                uniqueChoices.append(e)
        print("options", uniqueChoices)
        return ("options", param.dest)
    
    
"""     if (isinstance(param, argparse._StoreAction) and hasattr(param.type, "inx")):
            return param.type.inx(name, viewname, a) """

def argReader(box):
    for group in box.argparser._action_groups:
        for param in group._group_actions:
            dest = param.dest
            match dest:
                case "input"|"output"|"format"|"layout" :
                    print(dest)
                case _:
                    print(param.type,"-->", dest)
                    paramGetter(param)
                    


def run_generator(name, args):
    generators = generators_by_name()
    lower_name = name.lower()

    """ for gen in generators:
         print(gen) """

    if lower_name in generators.keys():
        box = generators[lower_name]()
        """ for a in dir(box):
             print(a) """
        argReader(box)
        box.parseArgs(args)
        box.open()
        box.render()
        box.close()

    else:
        msg = f'Unknown generator \'{name}\'. Use boxes --list to get a list of available commands.\n'
        print(msg)

def main() -> None:
        run_generator("ABox", ['--x=50', '--y=50', '--h=70', '--output=closedbox.svg'])

main()


#Le script fonctionne car il genere un fichier svg dans blenderboxes où est placé le fichier blend qui doit correspondre à une certaine source.
#Il faudrait maintenant s'interesser à la création d'un render particulier qui genererait soit un svg dans blender soit la création de curves/mesh au sein de blender.
 
#boxes closedbox --x=50 --y=50 --h=70 --output=closedbox.svg

