import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;

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
        JButton clearButton = new JButton("clear"); // New clear button

        // Add components to window
        frame.add(scroll, BorderLayout.CENTER);
        frame.add(saveButton, BorderLayout.SOUTH);
        frame.add(reloadButton, BorderLayout.NORTH);
        frame.add(clearButton, BorderLayout.EAST); // Added clear button to the right side

        // Save button action
        saveButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    // Let the user pick where to save
                    JFileChooser chooser = new JFileChooser();
                    int choice = chooser.showSaveDialog(frame);
                    
                    if (choice == JFileChooser.APPROVE_OPTION) {
                        File file = chooser.getSelectedFile();
                        FileWriter writer = new FileWriter(file);
                        writer.write(noteArea.getText());
                        writer.close();
                        JOptionPane.showMessageDialog(frame, "Note saved to " + file.getAbsolutePath());
                        noteArea.setText(""); // Clear text after saving
                    }
                } catch (Exception ex) {
                    JOptionPane.showMessageDialog(frame, "Error saving note");
                }
            }
        });

        // Reload button action
        reloadButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    // Let the user pick a file to load
                    JFileChooser chooser = new JFileChooser();
                    int choice = chooser.showOpenDialog(frame);
                    
                    if (choice == JFileChooser.APPROVE_OPTION) {
                        File file = chooser.getSelectedFile();
                        BufferedReader reader = new BufferedReader(new FileReader(file));
                        noteArea.setText("");
                        String line;
                        while ((line = reader.readLine()) != null) {
                            noteArea.append(line + "\n");
                        }
                        reader.close();
                        JOptionPane.showMessageDialog(frame, "Note loaded from " + file.getAbsolutePath());
                    }
                } catch (Exception ex) {
                    JOptionPane.showMessageDialog(frame, "Error loading note");
                }
            }
        });

        // Clear button action
        clearButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                noteArea.setText("");
            }
        });

        // Show the window
        frame.setVisible(true);
    }
}
