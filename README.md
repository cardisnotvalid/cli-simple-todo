# Simple Todo

```bash
# | ☐ | Name                   | Created            
3 | 𐄂 | Journal around 10 mins | 2024-05-20 16:42:54
2 | 𐄂 | 20 mins of yoga        | 2024-05-20 16:42:29
1 | 𐄂 | Brush teeth            | 2024-05-20 16:41:53
```

# Example

- Add
    ```bash
    python3 main.py add 'Vacuum Room'
    ```

    ```bash
    # | ☐ | Name        | Created            
    1 | 𐄂 | Vacuum Room | 2024-05-20 16:50:08
    ```

- Update
    ```bash
    python3 main.py update 1 --checked 
    ```

    ```bash
    # | ☐ | Name        | Created            
    1 | ✓ | Vacuum Room | 2024-05-20 16:50:08
    ```

- Delete
    ```bash
    python3 main.py delete 1 
    ```

    ```bash
    Todo list is empty
    ```
