class Execute():
    """Class to interpret and return correct output based on the tree from parser."""

    def __init__(self, tree, env):
        """Initiate variables before execution."""
        self.env = env
        self.tree = tree
        # Pass whole tree as argument.
        result = self.walkTree(tree)

        # Print result based on what walkTree returned.
        if result is not None and isinstance(result, int) or isinstance(result, float):
            print(result)
        if result is not None and isinstance(result, str):
            print(result)

    def walkTree(self, node):
        """
           Recursively call walkTree until tree is broken down to it's simplest form.
           Do this for all possible outcomes in the code received.
        """

        # First, if the node is None just return None.
        # (This happens if the user has typed something wrong)
        if node is None:
            return None

        # CLEAN RETURN STATEMENTS.
        if node[0] == 'num':
            return node[1]
        # For clean strings.
        if isinstance(node, str):
            return str(node[1:][:-1])

        # PRINT STRING AND EXPRESSIONS.
        if node[0] == 'print_str':
            return str(node[1][1:][:-1])
        elif node[0] == 'print_expr':
            return self.walkTree(node[1])
        
        # CONCATENATE STRINGS AND EXPRESSIONS WITH +.
        if node[0] == 'concatenate':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        
        # CONVERT OBJECT TO STRINGS.
        if node[0] == 'convert_str':
            # Return string of object.
            return str(self.walkTree(node[1]))

        # ADD, SUBTRACT, MULTIPLY AND DIVIDE
        if node[0] == 'add':
            # Recursively call walkTree until tree is broken down.
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            # Recursively call walkTree until tree is broken down.
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            # Recursively call walkTree until tree is broken down.
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            # Recursively call walkTree until tree is broken down.
            return self.walkTree(node[1]) / self.walkTree(node[2])
        
        # GET LOCAL VARIABLES FROM ENVIRONMENT.
        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '%s'" % node[1])
                # If undefined, return NOTHING in bytes.
                return b"\x00"

        # ASSIGN VARIABLES TO ENVIRONMENT.
        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
