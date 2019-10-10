// Demo Code for SerialCommand Library
// Steven Cogswell
// May 2011

#include <SerialCommand.h>
//#include <LinkedList.h>
#include <LoraAS32.h>

#define LORA_AUX_PIN 3 //External Interrupts: 2 and 3. 
#define LORA_MD0_PIN 4
#define LORA_MD1_PIN 5

SerialCommand sCmd;     // The demo SerialCommand object
LoraAS32 lora(&Serial1, LORA_AUX_PIN, LORA_MD0_PIN, LORA_MD1_PIN);

#define READ_BUFFER_LEN 24
char read_buffer_array[READ_BUFFER_LEN];
#include <Vector.h>
Vector<char> read_buffer;

void setup() {

  Serial.begin(9600);

  sCmd.addCommand("#", sharp_command); //組合指令
  sCmd.addCommand("$", dollar_command); //單一指令
  sCmd.addCommand("t", tx_command);
  sCmd.addCommand("setMode", setMode);
  sCmd.setDefaultHandler(unrecognized);      // Handler for command that isn't matched  (says "What?")

  //  lora.bypassAux();
  Serial1.begin(9600);
  lora.begin();
  Serial1.begin(9600);
  lora.setMode(LoraAS32::Normal);

  read_buffer.setStorage(read_buffer_array);
  Serial.println("Ready to receive...");
}



void print_read_buffer( ) {
  for (int x = 0; x < read_buffer.size(); x++) {
    Serial.print((char)read_buffer[x]);
  }
}

boolean print_binary_hex = false;

void loop() {
  sCmd.readSerial();     // We don't do much, just process serial commands
  if (Serial1.available()) {
    char read = Serial1.read();
    //    Serial.println(read_buffer.size());

    static boolean last_is_new_line = false;
    static boolean binary_mode = false;
    static int binary_count = 0;
    static int binary_size = 0;

    if (binary_mode  ) {
      if ( binary_count <= binary_size) {
        if (print_binary_hex) {
          if ( 0 <= read && read < 16) {
            Serial.print('0');
          }
          Serial.print((byte)read, HEX);
          Serial.print(' ');
        } else {
          Serial.print( read);
        }

        if ( 0  == (binary_count & 15) && 0 != binary_count ) {
//          Serial.println();
        }
      } else {
        Serial.println();
        binary_mode = false;
        Serial.println("***Leave binary mode***");
      }
    }
    else {
      if ( '\n' == read || read_buffer.size() >= (READ_BUFFER_LEN - 1)) {
        if (last_is_new_line) {
          Serial.print("rx: ");
          last_is_new_line = false;
        }

        String str_of_buffer = String(read_buffer_array);
        boolean start_with_bin = str_of_buffer.startsWith("bin");
        int str_length = str_of_buffer.length();

        if ( start_with_bin && 7 == str_length) {
          binary_mode = true;
          binary_count = 0;
          binary_size = atoi(str_of_buffer.substring(3).c_str());
          Serial.print(str_of_buffer);
          Serial.println(", binary mode, len: " + String(binary_size));
          Serial.println("***Enter binary mode***");
        } else {
          print_read_buffer();
          Serial.print((char)read);
        }

        read_buffer.clear();
        for (int x = 1; x < READ_BUFFER_LEN; x++) {
          read_buffer_array[x] = 0;
        }
        read_buffer_array[0] = '\0';

        if ('\n' == read) {
          last_is_new_line = true;
        }
      } else {

        read_buffer.push_back(read);
      }
    }

    if (binary_mode) {
      binary_count++;
    }

  }
}
