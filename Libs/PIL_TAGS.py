from PIL.ExifTags import Base

for i in range(1_000_000):
    Tag_id = i
    try:
        Tag_Name = Base(Tag_id).name
        print(f"TagID: {Tag_id} - {Tag_Name}")
    except:
        pass