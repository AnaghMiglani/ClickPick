import os

def upload_display_image(instance, filename):
    return os.path.join('stationery/display-images', filename)


def printout_rename(instance, filename):
    if instance.pk:
        ext = filename.split('.')[-1]
        new_name = '{}.{}'.format(instance.order_id, ext) 

        # when we move the record from active table to past table, then we first delete already present file like this
        for each_file in os.listdir(os.path.join('media/stationery/print-outs')):
            if (each_file == new_name):
                os.remove(os.path.join('media/stationery/print-outs', new_name))

        return os.path.join('stationery/print-outs', new_name)
    else:
        return filename


def printout_file_rename(instance, filename):
    """Rename files for PrintoutFile model - supports multiple files per printout"""
    import uuid
    from datetime import datetime
    
    # Get the printout order_id
    order_id = None
    if instance.printout_active:
        order_id = instance.printout_active.order_id
    elif instance.printout_past:
        order_id = instance.printout_past.order_id
    
    if order_id:
        ext = filename.split('.')[-1]
        # Create unique filename: order_id_timestamp_uuid.ext
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        new_name = f'{order_id}_{timestamp}_{unique_id}.{ext}'
        return os.path.join('stationery/print-outs', new_name)
    else:
        return os.path.join('stationery/print-outs', filename)
    
    
def temp_file_rename(instance, filename):
    return os.path.join('stationery/temp-files', filename)