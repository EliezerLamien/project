import javax.swing.*;      
import java.awt.*;     
import java.awt.event.*;
//import java.util.ArrayList;

public  class smart{
     public static void main(String[] args){
        JFrame frame=new JFrame("Smart Notes");
        frame.setSize(400,300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        //c
        JTextArea noteArea =new JTextArea(5,20);
        JScrollPane scrollPane=new JScrollPane(noteArea);

        JButton saveButton=new JButton("save Note");
        JButton addrelod=new JButton("relod");

        //add
        frame.add(scrollPane, BorderLayout.CENTER);
        frame.add(saveButton, BorderLayout.SOUTH);
        frame.add(addrelod,BorderLayout.NORTH);
        // 3. Add an action (listener) to the button
        saveButton.addActionListener(new ActionListener() {
    public void actionPerformed(ActionEvent e) {
        //System.out.println("You clicked Add Note!");
    }
});

        //frame.add(button);
        frame.setVisible(true);
        



     }
}