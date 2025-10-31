import os
from . import main
if __name__ == "__main__":
    main()
    
port = int(os.getenv("PORT", 8080))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

