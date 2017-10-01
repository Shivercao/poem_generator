import os
import tempfile


def obtain_paths():

    all_paths = {}

    all_paths['models_path'] = os.path.join(tempfile.gettempdir() , r'models')
    all_paths['int_dir'] = os.path.join(tempfile.gettempdir(), r'poems_by_author')
    all_paths['poems_dir'] = os.path.join(os.getcwd(), r'generatedPoems')

    if not os.path.exists(os.path.join(tempfile.gettempdir() , r'models')):
        os.makedirs(os.path.join(tempfile.gettempdir() , r'models'))
    if not os.path.exists(os.path.join(tempfile.gettempdir() , r'poems_by_author')):
        os.makedirs(os.path.join(tempfile.gettempdir() , r'poems_by_author'))
    if not os.path.exists(os.path.join(os.getcwd(), r'generatedPoems')):
        os.makedirs(os.path.join(os.getcwd(), r'generatedPoems'))

    return all_paths

