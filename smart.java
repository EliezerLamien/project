import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class smart {
    public static void main(String[] args) {
        // Create main window
        JFrame frame = new JFrame("Smart Notes");
        frame.setSize(400, 300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Create text area for typing notes
        JTextArea noteArea = new JTextArea();
        JScrollPane scroll = new JScrollPane(noteArea);

        // Create buttons
        JButton saveButton = new JButton("save");
        JButton reloadButton = new JButton("reload");

        // Add components to window
        frame.add(scroll, BorderLayout.CENTER);
        frame.add(saveButton, BorderLayout.SOUTH);
        frame.add(reloadButton, BorderLayout.NORTH);

        // Save button action
        saveButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    String text = noteArea.getText();
                    // Save text to file
                    java.io.FileWriter file = new java.io.FileWriter("notes.txt", true);
                    file.write(text + "\n----\n");
                    file.close();
                    JOptionPane.showMessageDialog(frame, "note saved");
                    noteArea.setText(""); // clear text after saving
                } catch (Exception ex) {
                    JOptionPane.showMessageDialog(frame, "error saving note");
                }
            }
        });

        // Reload button action
        reloadButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    // Read notes from file
                    java.io.BufferedReader read = new java.io.BufferedReader(new java.io.FileReader("notes.txt"));
                    noteArea.setText(""); // clear before loading
                    String line;
                    while ((line = read.readLine()) != null) {
                        noteArea.append(line + "\n");
                    }
                    read.close();
                } catch (Exception ex) {
                    JOptionPane.showMessageDialog(frame, "no notes yet");
                }
            }
        });

        // Show the window
        frame.setVisible(true);
    }
}
