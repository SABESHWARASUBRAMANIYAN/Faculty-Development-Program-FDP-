
import java.io.*;
import java.util.*;
import java.nio.file.*;

 class FileManipulationMenu{
public static void main(String[] args) {
Scanner scanner = new Scanner(System.in);
boolean exit = false;

while (!exit) {
System.out.println("File Manipulation Menu:");
System.out.println("1. Get specific files with extensions from a folder");
System.out.println("2. Check if a file or directory exists");
System.out.println("3. Check read and write permissions");
System.out.println("4. Check if pathname is a directory or file");
System.out.println("5. Compare two files lexicographically");
System.out.println("6. Get last modified date of a file");
System.out.println("7. Read input from console");
System.out.println("8. Get file size");
System.out.println("9. Read file content into a byte array");
System.out.println("10. Read file content line by line");
System.out.println("11. Read a plain text file");
System.out.println("12. Read file line by line and store in a variable");
System.out.println("13. Store text file content line by line in an array");
System.out.println("14. Write and read a plain text file");
System.out.println("15. Append text to an existing file");
System.out.println("16. Read the first 3 lines of a file");
System.out.println("17. Find the longest word in a text file");
System.out.println("18. Get a list of all file/directory names in a directory");
System.out.println("19. Exit");

System.out.print("Enter your choice: ");
int choice = scanner.nextInt();
scanner.nextLine(); // Consume the newline character

switch (choice) {
case 1:
getFilesWithExtensions();
break;
case 2:
checkFileOrDirectoryExists();
break;
case 3:
checkReadWritePermissions();
break;
case 4:
checkDirectoryOrFile();
break;
case 5:
compareFilesLexicographically();
break;
case 6:
getLastModifiedDate();
break;
case 7:
readInputFromConsole();
break;
case 8:
getFileSize();
break;
case 9:
readFileIntoByteArray();
break;
case 10:
readFileLineByLine();
break;
case 11:
readPlainTextFile();
break;
case 12:
readFileLineByLineIntoVariable();
break;
case 13:
storeTextFileContentInArray();
break;
case 14:
writeAndReadPlainTextFile();
break;
case 15:
appendTextToFile();
break;
case 16:
readFirstThreeLinesOfFile();
break;
case 17:
findLongestWordInFile();
break;
case 18:
listFilesInDirectory();
break;
case 19:
exit = true;
break;
default:
System.out.println("Invalid choice. Please enter a valid option.");
}
}

scanner.close();
}

private static Scanner scanner = new Scanner(System.in);

// 1. Get specific files with extensions from a folder
private static void getFilesWithExtensions() {
System.out.print("Enter folder path: ");
String folderPath = scanner.nextLine();
System.out.print("Enter file extension (e.g., '.txt'): ");
String extension = scanner.nextLine();

File folder = new File(folderPath);
File[] files = folder.listFiles((dir, name) -> name.endsWith(extension));

if (files != null) {
for (File file : files) {
System.out.println(file.getName());
}
} else {
System.out.println("Folder does not exist or is empty.");
}
}

// 2. Check if a file or directory exists
private static void checkFileOrDirectoryExists() {
System.out.print("Enter file or directory path: ");
String path = scanner.nextLine();

File fileOrDir = new File(path);
if (fileOrDir.exists()) {
System.out.println("File or directory exists.");
} else {
System.out.println("File or directory does not exist.");
}
}

// 3. Check read and write permissions
private static void checkReadWritePermissions() {
System.out.print("Enter file or directory path: ");
String path = scanner.nextLine();

File fileOrDir = new File(path);
if (fileOrDir.exists()) {
if (fileOrDir.canRead() && fileOrDir.canWrite()) {
System.out.println("Read and write permissions are granted.");
} else {
System.out.println("Read and/or write permissions are not granted.");
}
} else {
System.out.println("File or directory does not exist.");
}
}

// 4. Check if pathname is a directory or file
private static void checkDirectoryOrFile() {
System.out.print("Enter file or directory path: ");
String path = scanner.nextLine();

File fileOrDir = new File(path);
if (fileOrDir.exists()) {
if (fileOrDir.isDirectory()) {
System.out.println("Path is a directory.");
} else if (fileOrDir.isFile()) {
System.out.println("Path is a file.");
}
} else {
System.out.println("File or directory does not exist.");
}
}

// 5. Compare two files lexicographically
private static void compareFilesLexicographically() {
System.out.print("Enter path of the first file: ");
String path1 = scanner.nextLine();
System.out.print("Enter path of the second file: ");
String path2 = scanner.nextLine();

File file1 = new File(path1);
File file2 = new File(path2);

try {
Scanner reader1 = new Scanner(file1);
Scanner reader2 = new Scanner(file2);

while (reader1.hasNextLine() && reader2.hasNextLine()) {
String line1 = reader1.nextLine();
String line2 = reader2.nextLine();
if (!line1.equals(line2)) {
System.out.println("Files are not equal.");
return;
}
}

if (!reader1.hasNextLine() && !reader2.hasNextLine()) {
System.out.println("Files are equal.");
} else {
System.out.println("Files have different lengths.");
}

reader1.close();
reader2.close();
} catch (IOException e) {
System.out.println("Error reading files.");
}
}

// 6. Get last modified date of a file
private static void getLastModifiedDate() {
System.out.print("Enter file path: ");
String path = scanner.nextLine();

File file = new File(path);
if (file.exists()) {
long lastModified = file.lastModified();
Date date = new Date(lastModified);
System.out.println("Last modified date: " + date);
} else {
System.out.println("File does not exist.");
}
}

// 7. Read input from console
private static void readInputFromConsole() {
System.out.print("Enter a line of text: ");
String input = scanner.nextLine();
System.out.println("You entered: " + input);
}

// 8. Get file size
private static void getFileSize() {
System.out.print("Enter file path: ");
String path = scanner.nextLine();

File file = new File(path);
if (file.exists()) {
long fileSize = file.length();
System.out.println("File size: " + fileSize + " bytes");
System.out.println("File size: " + (fileSize / 1024) + " KB");
System.out.println("File size: " + (fileSize / (1024 * 1024)) + " MB");
} else {
System.out.println("File does not exist.");
}
}

// 9. Read file content into a byte array
private static void readFileIntoByteArray() {
System.out.print("Enter file path: ");
String path = scanner.nextLine();

File file = new File(path);
if (file.exists()) {
try {
byte[] fileBytes = Files.readAllBytes(file.toPath());
System.out.println("File content as bytes: " + Arrays.toString(fileBytes));
} catch (IOException e) {
System.out.println("Error reading file.");
}
} else {
System.out.println("File does not exist.");
}
}

// 10. Read file content line by line
private static void readFileLineByLine() {
System.out.print("Enter file path: ");
String path = scanner.nextLine();

File file = new File(path);
if (file.exists()) {
try {
Scanner fileScanner = new Scanner(file);
while (fileScanner.hasNextLine()) {
String line = fileScanner.nextLine();
System.out.println(line);
}
fileScanner.close();
} catch (IOException e) {
System.out.println("Error reading file.");
}
} else {
System.out.println("File does not exist.");
}
}

// 11. Read a plain text file
private static void readPlainTextFile() {
System.out.print("Enter file path: ");
String path = scanner.nextLine();

File file = new File(path);
if (file.exists()) {
try {
BufferedReader reader = new BufferedReader(new FileReader(file));
String line;
while ((line = reader.readLine()) != null) {
System.out.println(line);
}
reader.close();
} catch (IOException e) {
System.out.println("Error reading file.");
}
} else {
System.out.println("File does not exist.");
}
}

// 12. Read file line by line and store in a variable
private static void readFileLineByLineIntoVariable() {
System.out.print("Enter file path: ");
String path = scanner.nextLine();

File file = new File(path);
if (file.exists()) {
try {
StringBuilder content = new StringBuilder();
BufferedReader reader = new BufferedReader(new FileReader(file));
String line;
while ((line = reader.readLine()) != null) {
content.append(line).append("\n");
}
reader.close();
System.out.println("File content:\n" + content.toString());
} catch (IOException e) {
System.out.println("Error reading file.");
}
} else {
System.out.println("File does not exist.");
}
}

// 13. Store text file content line by line in an array
private static void storeTextFileContentInArray() {
System.out.print("Enter file path: ");
String path = scanner.nextLine();

File file = new File(path);
if (file.exists()) {
try {
ArrayList<String> lines = new ArrayList<>();
BufferedReader reader = new BufferedReader(new FileReader(file));
String line;
while ((line = reader.readLine()) != null) {
lines.add(line);
}
reader.close();
System.out.println("File content stored in an array:");
for (String fileLine : lines) {
System.out.println(fileLine);
}
} catch (IOException e) {
System.out.println("Error reading file.");
}
} else {
System.out.println("File does not exist.");
}
}

// 14. Write and read a plain text file
private static void writeAndReadPlainTextFile() {
System.out.print("Enter file path to write: ");
String path = scanner.nextLine();
System.out.print("Enter content to write to the file: ");
String content = scanner.nextLine();

try {
FileWriter writer = new FileWriter(path);
writer.write(content);
writer.close();
System.out.println("Content written to the file.");

// Read and display the content
System.out.println("Reading the file content:");
BufferedReader reader = new BufferedReader(new FileReader(path));
String line;
while ((line = reader.readLine()) != null) {
System.out.println(line);
}
reader.close();
} catch (IOException e) {
System.out.println("Error writing/reading file.");
}
}

// 15. Append text to an existing file
private static void appendTextToFile() {
System.out.print("Enter file path to append: ");
String path = scanner.nextLine();
System.out.print("Enter content to append to the file: ");
String content = scanner.nextLine();

try {
FileWriter writer = new FileWriter(path, true); // Set append mode to true
writer.write(content);
writer.close();
System.out.println("Content appended to the file.");

// Read and display the updated content
System.out.println("Reading the updated file content:");
BufferedReader reader = new BufferedReader(new FileReader(path));
String line;
while ((line = reader.readLine()) != null) {
System.out.println(line);
}
reader.close();
} catch (IOException e) {
System.out.println("Error appending/reading file.");
}
}

// 16. Read the first 3 lines of a file
private static void readFirstThreeLinesOfFile() {
System.out.print("Enter file path: ");
String path = scanner.nextLine();

File file = new File(path);
if (file.exists()) {
try {
BufferedReader reader = new BufferedReader(new FileReader(file));
String line;
int lineCount = 0;
while ((line = reader.readLine()) != null && lineCount < 3) {
System.out.println(line);
lineCount++;
}
reader.close();
} catch (IOException e) {
System.out.println("Error reading file.");
}
} else {
System.out.println("File does not exist.");
}
}

// 17. Find the longest word in a text file
private static void findLongestWordInFile() {
System.out.print("Enter file path: ");
String path = scanner.nextLine();

File file = new File(path);
if (file.exists()) {
try {
BufferedReader reader = new BufferedReader(new FileReader(file));
String line;
String longestWord = "";
while ((line = reader.readLine()) != null) {
String[] words = line.split("\\s+");
for (String word : words) {
if (word.length() > longestWord.length()) {
longestWord = word;
}
}
}
reader.close();

if (!longestWord.isEmpty()) {
System.out.println("Longest word: " + longestWord);
} else {
System.out.println("No words found in the file.");
}
} catch (IOException e) {
System.out.println("Error reading file.");
}
} else {
System.out.println("File does not exist.");
}
}

// 18. Get a list of all file/directory names in a directory
private static void listFilesInDirectory() {
System.out.print("Enter directory path: ");
String directoryPath = scanner.nextLine();

File directory = new File(directoryPath);
if (directory.exists() && directory.isDirectory()) {
File[] files = directory.listFiles();
if (files != null) {
System.out.println("List of files/directories in the directory:");
for (File file : files) {
System.out.println(file.getName());
}
} else {
System.out.println("Directory is empty.");
}
} else {
System.out.println("Directory does not exist.");
}
}
}


	