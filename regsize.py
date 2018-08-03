import winreg

# Node data structure
class Node:
	def __init__(self, parent, key):
		self.parent = parent
		self.key = key
		self.count = 0
		self.childs = []

	def path(self):
		path = self.key
		currentParent = self.parent
		while (currentParent is not None):
			path = currentParent.key + "\\" + path
			currentParent = currentParent.parent
		return path

# Hive scanning entry code
def scanHive(name, rootNode, hkeyConstant, path):
	with winreg.OpenKey(hkeyConstant, path) as handle:
		hiveNode = Node(rootNode, name)
		rootNode.childs.append(hiveNode)
		processNode(hiveNode, handle)

# Node processing code
def processNode(node, handle):
	# Retrieve stats about this key
	numSubkeys, numValues = winreg.QueryInfoKey(handle)[0:2]

	# Enumerate values
	for i in range(0, numValues):
		valueName, valueData = winreg.EnumValue(handle, i)[0:2]

		# Add the number of characters in the value name and data to the count of this node
		node.count += len(valueName);
		node.count += len(str(valueData))

	# Enumerate subkeys
	for i in range(0, numSubkeys):
		subkeyName = winreg.EnumKey(handle, i)

		if subkeyName == "Wow6432Node":
			# Keys with this name are for backward compatibility and work as symbolic links to other parts of the registry.
			# We skip them so we don't count these nodes more than once
			continue

		# Recurse
		try:
			with winreg.OpenKey(handle, subkeyName) as childHandle:

				# Add child node
				child = Node(node, subkeyName)
				node.childs.append(child)

				# Add the number of characters in the subkey name to the count of its node
				child.count += len(subkeyName)

				# Process the child node
				processNode(child, childHandle)

		except PermissionError as error:
			print("Warning: Access denied: " + node.path() + ". Ignoring subkey.")

# Node count summing code
def sumCounts(node):
	for child in node.childs:
		sumCounts(child)
		node.count += child.count

# Node printing code
def printNode(node, prefix, childPrefix, threshold):
	# Print the output for this node
	print(prefix + node.key + " [" + "{:,}".format(node.count) + "]")

	# Make a list of children to print. We need to do this before actually printing them, in order to format the output correctly.
	childsToPrint = []
	for child in node.childs:
		if (child.count > threshold):
			childsToPrint.append(child)

	# Sort the list by size
	childsToPrint.sort(key=lambda node: -node.count)

	# Print the childs by recursion
	for index, child in enumerate(childsToPrint):

		# Print spacing line for readability if the previous child printed any children
		print(childPrefix + "|")

		newChildPrefix = childPrefix + ("|  " if (index < len(childsToPrint) - 1) else "   ")
		printNode(child, childPrefix + "+--", newChildPrefix, threshold)

# Perform scan
root = Node(None, "Scanned paths")

scanHive("HKEY_LOCAL_MACHINE\\SOFTWARE", root, winreg.HKEY_LOCAL_MACHINE, "SOFTWARE")
scanHive("HKEY_CURRENT_USER", root, winreg.HKEY_CURRENT_USER, "")

# Print results
displayThreshold = 10

sumCounts(root)
printNode(root, "", "", root.count / displayThreshold)