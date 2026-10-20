"""Built-in sample questions used when no AI API key is available.

Each question has four options, a zero-based correct answer index, and a
short explanation. The app picks the most relevant bank by keyword matching.
"""

SAMPLE_BANKS = [
    {
        "name": "Python Programming",
        "keywords": [
            "python", "django", "flask", "pandas", "numpy", "function",
            "list", "dictionary", "tuple", "loop", "exception",
        ],
        "questions": [
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": ["def", "function", "fun", "define"],
                "answer": 0,
                "explanation": "Functions in Python are defined with the 'def' keyword, "
                "followed by the function name and parentheses.",
            },
            {
                "question": "What is the output of len(\"Python\")?",
                "options": ["5", "6", "7", "Error"],
                "answer": 1,
                "explanation": "The string \"Python\" contains six characters, so len() returns 6.",
            },
            {
                "question": "Which of these Python data types is immutable?",
                "options": ["list", "dictionary", "set", "tuple"],
                "answer": 3,
                "explanation": "Tuples cannot be changed after creation. Lists, dictionaries, "
                "and sets are mutable.",
            },
            {
                "question": "Which symbol starts a single-line comment in Python?",
                "options": ["//", "#", "/*", "--"],
                "answer": 1,
                "explanation": "Anything after a '#' on a line is treated as a comment by Python.",
            },
            {
                "question": "What does range(1, 5) produce?",
                "options": [
                    "1, 2, 3, 4, 5",
                    "1, 2, 3, 4",
                    "0, 1, 2, 3, 4",
                    "2, 3, 4, 5",
                ],
                "answer": 1,
                "explanation": "The stop value in range() is excluded, so range(1, 5) gives "
                "1, 2, 3, and 4.",
            },
            {
                "question": "Which list method adds an item to the end of a list?",
                "options": ["add()", "insert()", "append()", "push()"],
                "answer": 2,
                "explanation": "list.append(item) adds the item to the end of the list. "
                "insert() adds at a specific position.",
            },
            {
                "question": "What is the result of 10 // 3 in Python?",
                "options": ["3.33", "3", "4", "1"],
                "answer": 1,
                "explanation": "The // operator performs floor division, so 10 // 3 is 3.",
            },
            {
                "question": "Which statement is used to handle exceptions in Python?",
                "options": ["try/except", "if/else", "for/while", "switch/case"],
                "answer": 0,
                "explanation": "Code that may raise an error is placed in a try block, and the "
                "error is handled in an except block.",
            },
        ],
    },
    {
        "name": "Data Structures",
        "keywords": [
            "data structure", "data structures", "stack", "queue", "linked list",
            "binary tree", "bst", "graph", "heap", "hashing", "array",
        ],
        "questions": [
            {
                "question": "Which data structure follows the Last-In, First-Out (LIFO) principle?",
                "options": ["Queue", "Stack", "Linked list", "Graph"],
                "answer": 1,
                "explanation": "In a stack, the most recently added element is removed first, "
                "which is the LIFO principle.",
            },
            {
                "question": "Which data structure follows the First-In, First-Out (FIFO) principle?",
                "options": ["Stack", "Tree", "Queue", "Set"],
                "answer": 2,
                "explanation": "A queue removes elements in the same order they were inserted, "
                "so it follows FIFO.",
            },
            {
                "question": "Which traversal of a binary search tree visits nodes in sorted order?",
                "options": ["Pre-order", "Post-order", "Level-order", "In-order"],
                "answer": 3,
                "explanation": "In-order traversal visits the left subtree, then the node, then "
                "the right subtree, producing sorted values in a BST.",
            },
            {
                "question": "What is the time complexity of binary search on a sorted array?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                "answer": 1,
                "explanation": "Binary search halves the search range on each step, giving "
                "O(log n) time complexity.",
            },
            {
                "question": "Which data structure stores data as key-value pairs?",
                "options": ["Array", "Stack", "Hash table", "Queue"],
                "answer": 2,
                "explanation": "A hash table maps keys to values and provides fast average-case "
                "lookup using a hash function.",
            },
            {
                "question": "Which data structure is commonly used to implement breadth-first search (BFS)?",
                "options": ["Stack", "Queue", "Heap", "Set"],
                "answer": 1,
                "explanation": "BFS explores nodes level by level and uses a queue to process "
                "nodes in the order they are discovered.",
            },
            {
                "question": "What is a key advantage of a linked list over an array?",
                "options": [
                    "Constant-time random access",
                    "Dynamic size and easier insertion",
                    "Less memory per element",
                    "Built-in sorting",
                ],
                "answer": 1,
                "explanation": "A linked list can grow or shrink dynamically and inserting a node "
                "does not require shifting all later elements.",
            },
            {
                "question": "What is the worst-case search time in an unbalanced binary search tree?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
                "answer": 2,
                "explanation": "If the tree becomes a straight chain, searching may visit every "
                "node, giving O(n) worst-case time.",
            },
        ],
    },
    {
        "name": "Database Management Systems",
        "keywords": [
            "dbms", "database", "sql", "normalization", "primary key", "foreign key",
            "acid", "transaction", "relational", "mysql", "oracle",
        ],
        "questions": [
            {
                "question": "Which SQL command is used to retrieve data from a table?",
                "options": ["SELECT", "INSERT", "UPDATE", "DELETE"],
                "answer": 0,
                "explanation": "SELECT queries data from one or more tables. The other commands "
                "modify the data.",
            },
            {
                "question": "Which property must a primary key satisfy?",
                "options": [
                    "It may contain duplicate values",
                    "It must be unique and not NULL",
                    "It must always be a string",
                    "It can reference another table",
                ],
                "answer": 1,
                "explanation": "A primary key uniquely identifies each row, so it cannot contain "
                "duplicates or NULL values.",
            },
            {
                "question": "What is the main goal of database normalization?",
                "options": [
                    "Increase data redundancy",
                    "Reduce data redundancy and anomalies",
                    "Encrypt all tables",
                    "Delete old records",
                ],
                "answer": 1,
                "explanation": "Normalization organizes tables to reduce redundancy and avoid "
                "insertion, update, and deletion anomalies.",
            },
            {
                "question": "Which normal form removes partial dependencies on a composite key?",
                "options": ["1NF", "2NF", "3NF", "BCNF"],
                "answer": 1,
                "explanation": "Second Normal Form (2NF) requires 1NF and removes partial "
                "dependencies of non-key attributes on part of a composite key.",
            },
            {
                "question": "Which SQL clause filters groups created by GROUP BY?",
                "options": ["WHERE", "HAVING", "ORDER BY", "LIMIT"],
                "answer": 1,
                "explanation": "HAVING filters grouped results, while WHERE filters individual "
                "rows before grouping.",
            },
            {
                "question": "A foreign key in one table normally references what in another table?",
                "options": [
                    "Any text column",
                    "The primary key",
                    "A temporary table",
                    "An index name",
                ],
                "answer": 1,
                "explanation": "A foreign key references a primary key (or unique key) in another "
                "table to enforce referential integrity.",
            },
            {
                "question": "In ACID properties, what does the 'A' stand for?",
                "options": ["Atomicity", "Availability", "Access", "Aggregation"],
                "answer": 0,
                "explanation": "ACID stands for Atomicity, Consistency, Isolation, and Durability. "
                "Atomicity means a transaction is all-or-nothing.",
            },
            {
                "question": "Which join returns only rows with matching values in both tables?",
                "options": ["LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "INNER JOIN"],
                "answer": 3,
                "explanation": "INNER JOIN returns only the rows where the join condition matches "
                "in both tables.",
            },
        ],
    },
    {
        "name": "Artificial Intelligence",
        "keywords": [
            "artificial intelligence", "machine learning", "deep learning",
            "neural network", "ai", "ml", "nlp", "data science", "turing test",
            "reinforcement learning", "supervised learning",
        ],
        "questions": [
            {
                "question": "What does AI stand for?",
                "options": [
                    "Automatic Information",
                    "Artificial Intelligence",
                    "Advanced Internet",
                    "Applied Integration",
                ],
                "answer": 1,
                "explanation": "AI stands for Artificial Intelligence, the field of building "
                "systems that perform tasks requiring human-like intelligence.",
            },
            {
                "question": "Which type of machine learning uses labeled training data?",
                "options": [
                    "Unsupervised learning",
                    "Reinforcement learning",
                    "Supervised learning",
                    "Clustering",
                ],
                "answer": 2,
                "explanation": "Supervised learning trains a model on input-output pairs where the "
                "correct output (label) is provided.",
            },
            {
                "question": "Which of these is a classification problem?",
                "options": [
                    "Predicting a house price",
                    "Detecting whether an email is spam",
                    "Grouping customers by behavior",
                    "Reducing image dimensions",
                ],
                "answer": 1,
                "explanation": "Spam detection assigns an email to a discrete class (spam or not "
                "spam), which makes it a classification task.",
            },
            {
                "question": "What does overfitting mean in machine learning?",
                "options": [
                    "The model performs poorly on training data",
                    "The model performs well on training data but poorly on new data",
                    "The model has too few parameters",
                    "The data has no features",
                ],
                "answer": 1,
                "explanation": "An overfitted model memorizes the training data, including noise, "
                "and therefore generalizes poorly to unseen data.",
            },
            {
                "question": "Which algorithm is commonly used for clustering?",
                "options": ["Linear regression", "K-means", "Logistic regression", "Naive Bayes"],
                "answer": 1,
                "explanation": "K-means groups data points into k clusters based on similarity, "
                "making it an unsupervised clustering algorithm.",
            },
            {
                "question": "What does NLP mainly deal with?",
                "options": [
                    "Computer hardware",
                    "Human language and text",
                    "Network routing",
                    "Database storage",
                ],
                "answer": 1,
                "explanation": "Natural Language Processing (NLP) enables computers to understand, "
                "interpret, and generate human language.",
            },
            {
                "question": "What is the purpose of the Turing test?",
                "options": [
                    "To measure processor speed",
                    "To check whether a machine can exhibit intelligent behavior",
                    "To encrypt messages",
                    "To train neural networks",
                ],
                "answer": 1,
                "explanation": "The Turing test evaluates whether a machine's responses are "
                "indistinguishable from those of a human.",
            },
            {
                "question": "How does reinforcement learning improve an agent's behavior?",
                "options": [
                    "By using labeled examples only",
                    "By receiving rewards and penalties",
                    "By sorting data",
                    "By compressing images",
                ],
                "answer": 1,
                "explanation": "A reinforcement learning agent learns by taking actions and "
                "receiving rewards or penalties from the environment.",
            },
        ],
    },
    {
        "name": "Computer Networks",
        "keywords": [
            "computer network", "networking", "tcp", "ip", "osi", "router", "dns",
            "http", "lan", "wan", "protocol", "topology",
        ],
        "questions": [
            {
                "question": "How many layers are there in the OSI reference model?",
                "options": ["4", "5", "6", "7"],
                "answer": 3,
                "explanation": "The OSI model has seven layers: Physical, Data Link, Network, "
                "Transport, Session, Presentation, and Application.",
            },
            {
                "question": "Which device routes packets between different networks?",
                "options": ["Hub", "Switch", "Router", "Repeater"],
                "answer": 2,
                "explanation": "A router uses IP addresses to forward packets between networks.",
            },
            {
                "question": "What is the default port number for HTTP?",
                "options": ["21", "25", "80", "443"],
                "answer": 2,
                "explanation": "HTTP uses port 80 by default, while HTTPS uses port 443.",
            },
            {
                "question": "What is the main function of DNS?",
                "options": [
                    "Encrypt network traffic",
                    "Translate domain names into IP addresses",
                    "Assign MAC addresses",
                    "Compress files",
                ],
                "answer": 1,
                "explanation": "The Domain Name System (DNS) resolves human-readable domain names "
                "such as example.com into IP addresses.",
            },
            {
                "question": "Which transport protocol provides reliable, connection-oriented delivery?",
                "options": ["UDP", "TCP", "IP", "ICMP"],
                "answer": 1,
                "explanation": "TCP establishes a connection and uses acknowledgments and "
                "retransmission to provide reliable delivery.",
            },
            {
                "question": "What does LAN stand for?",
                "options": [
                    "Large Area Network",
                    "Local Area Network",
                    "Long Access Node",
                    "Linked Access Network",
                ],
                "answer": 1,
                "explanation": "A LAN (Local Area Network) connects devices within a limited area, "
                "such as a home, office, or campus.",
            },
            {
                "question": "Which protocol securely transfers web pages?",
                "options": ["HTTP", "FTP", "HTTPS", "SMTP"],
                "answer": 2,
                "explanation": "HTTPS uses TLS/SSL encryption to secure data sent between a browser "
                "and a web server.",
            },
            {
                "question": "In a star topology, how are devices connected?",
                "options": [
                    "In a single ring",
                    "To a central hub or switch",
                    "Directly to every other device",
                    "Through a shared bus only",
                ],
                "answer": 1,
                "explanation": "A star topology connects each device to a central hub or switch, "
                "which manages communication between them.",
            },
        ],
    },
    {
        "name": "Operating Systems",
        "keywords": [
            "operating system", "os", "process", "thread", "scheduling", "deadlock",
            "virtual memory", "paging", "kernel", "semaphore",
        ],
        "questions": [
            {
                "question": "What is the primary role of an operating system?",
                "options": [
                    "Create web pages",
                    "Manage hardware and software resources",
                    "Design databases",
                    "Compile source code",
                ],
                "answer": 1,
                "explanation": "An operating system manages CPU, memory, storage, and I/O devices, "
                "and provides services for application programs.",
            },
            {
                "question": "Which scheduling algorithm runs processes in arrival order?",
                "options": [
                    "Shortest Job First",
                    "Round Robin",
                    "First Come, First Served",
                    "Priority Scheduling",
                ],
                "answer": 2,
                "explanation": "First Come, First Served (FCFS) executes processes in the order "
                "they arrive in the ready queue.",
            },
            {
                "question": "Which condition is necessary for a deadlock?",
                "options": [
                    "Preemption of all resources",
                    "Circular wait",
                    "Unlimited memory",
                    "Single process execution",
                ],
                "answer": 1,
                "explanation": "Deadlock requires four conditions, including circular wait, where "
                "each process waits for a resource held by another in the cycle.",
            },
            {
                "question": "What does virtual memory allow?",
                "options": [
                    "Programs larger than physical memory to run",
                    "Faster CPU clock speeds",
                    "Permanent deletion of files",
                    "Direct access to the BIOS",
                ],
                "answer": 0,
                "explanation": "Virtual memory uses disk space as an extension of RAM, allowing "
                "programs whose total size exceeds physical memory to execute.",
            },
            {
                "question": "Which of the following is NOT an operating system?",
                "options": ["Windows", "Linux", "macOS", "Oracle"],
                "answer": 3,
                "explanation": "Oracle is a database management system, while Windows, Linux, and "
                "macOS are operating systems.",
            },
            {
                "question": "What is a key difference between a process and a thread?",
                "options": [
                    "Threads share the process's memory space",
                    "Processes cannot run concurrently",
                    "Threads always have their own address space",
                    "Processes are always faster",
                ],
                "answer": 0,
                "explanation": "Threads within the same process share memory and resources, whereas "
                "separate processes have independent address spaces.",
            },
            {
                "question": "What causes thrashing in an operating system?",
                "options": [
                    "Too little paging activity",
                    "Excessive paging and memory pressure",
                    "Using a single process",
                    "Disabling virtual memory",
                ],
                "answer": 1,
                "explanation": "Thrashing occurs when the system spends most of its time swapping "
                "pages in and out instead of executing useful work.",
            },
            {
                "question": "What is a semaphore used for?",
                "options": [
                    "Synchronizing processes and controlling access to shared resources",
                    "Compiling programs",
                    "Storing files permanently",
                    "Assigning IP addresses",
                ],
                "answer": 0,
                "explanation": "Semaphores are synchronization primitives used to coordinate "
                "processes and protect shared resources.",
            },
        ],
    },
    {
        "name": "General Knowledge",
        "keywords": [
            "general knowledge", "gk", "history", "geography", "science",
            "world war", "capital", "planet", "current affairs",
        ],
        "questions": [
            {
                "question": "What is the capital of France?",
                "options": ["Berlin", "Madrid", "Paris", "Rome"],
                "answer": 2,
                "explanation": "Paris is the capital and largest city of France.",
            },
            {
                "question": "Which is the largest planet in our solar system?",
                "options": ["Earth", "Jupiter", "Saturn", "Neptune"],
                "answer": 1,
                "explanation": "Jupiter is the largest planet in the solar system by both mass and "
                "diameter.",
            },
            {
                "question": "What is the chemical formula for water?",
                "options": ["CO2", "H2O", "O2", "NaCl"],
                "answer": 1,
                "explanation": "Water is made of two hydrogen atoms and one oxygen atom, giving "
                "the formula H2O.",
            },
            {
                "question": "Who wrote the play 'Romeo and Juliet'?",
                "options": [
                    "Charles Dickens",
                    "William Shakespeare",
                    "Jane Austen",
                    "Mark Twain",
                ],
                "answer": 1,
                "explanation": "William Shakespeare wrote the tragedy 'Romeo and Juliet' in the "
                "late 16th century.",
            },
            {
                "question": "Which is the largest ocean on Earth?",
                "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
                "answer": 3,
                "explanation": "The Pacific Ocean is the largest and deepest of Earth's oceans.",
            },
            {
                "question": "What is the smallest prime number?",
                "options": ["0", "1", "2", "3"],
                "answer": 2,
                "explanation": "A prime number has exactly two factors. 2 is the smallest prime "
                "number and the only even prime.",
            },
            {
                "question": "What is the currency of Japan?",
                "options": ["Won", "Yuan", "Yen", "Ringgit"],
                "answer": 2,
                "explanation": "The Japanese yen is the official currency of Japan.",
            },
            {
                "question": "In which year did World War II end?",
                "options": ["1918", "1939", "1945", "1950"],
                "answer": 2,
                "explanation": "World War II ended in 1945 after the surrender of Germany and Japan.",
            },
        ],
    },
]
