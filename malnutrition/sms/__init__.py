class Command:
    """ A command is a general wrapper around the thing SMS does. It looks like there
    is a basic structure:
    
        COMMAND some text
    
    We always need to do the following (pretty much):
    
        - find the write view for the command
        
        - take the text and pass it into a form
        
        - validate form
        
        - do something if it works
        
        - do something if it fails
    """
    