
void setMode() {
  char*arg = sCmd.next();
  if (arg != NULL) {
    int mode = atoi(arg);
    lora.setMode((LoraAS32::Mode)mode);
    Serial.println("setMode: " + String(mode));
  }
}

void processCommand() {
  int aNumber;
  char *arg;

  Serial.println("We're in processCommand");
  arg = sCmd.next();
  if (arg != NULL) {
    aNumber = atoi(arg);    // Converts a char string to an integer
    Serial.print("First argument was: ");
    Serial.println(aNumber);
  }
  else {
    Serial.println("No arguments");
  }

  arg = sCmd.next();
  if (arg != NULL) {
    aNumber = atol(arg);
    Serial.print("Second argument was: ");
    Serial.println(aNumber);
  }
  else {
    Serial.println("No second argument");
  }
}

void air_speed_command(String speed) {
  boolean ok = false;
  if (speed.equals("0.3")) {
    lora.setAirSpeed(LoraAS32::_0_3bps);
    ok = true;
  } else if (speed.equals("1.2")) {
    lora.setAirSpeed(LoraAS32::_1_2bps);
    ok = true;
  } else if (speed.equals("2.4")) {
    lora.setAirSpeed(LoraAS32::_2_4bps);
    ok = true;
  } else if (speed.equals("4.8")) {
    lora.setAirSpeed(LoraAS32::_4_8bps);
    ok = true;
  } else if (speed.equals("9.6")) {
    lora.setAirSpeed(LoraAS32::_9_6bps);
    ok = true;
  } else if (speed.equals("19.2")) {
    lora.setAirSpeed(LoraAS32::_19_2bps);
    ok = true;
  }

  if (ok) {
    Serial.println("air_speed_command: " + String(speed));
  } else {

  }
}

void air_speed_command_done(String speed) {
  air_speed_command(speed);
  delay(45);
  bool store_result = lora.storeSettingToSram();
  lora.setMode(LoraAS32::Normal);
  if (!store_result) {
    Serial.println("store to sram failed");
  }
}


void tx_power_command(String power) {
  boolean ok = false;
  if (power.equals("0")) {
    lora.setTransmissionPower(LoraAS32::_30dBm);
    ok = true;
  } else if (power.equals("1")) {
    lora.setTransmissionPower(LoraAS32::_27dBm);
    ok = true;
  } else if (power.equals("2")) {
    lora.setTransmissionPower(LoraAS32::_24dBm);
    ok = true;
  } else if (power.equals("3")) {
    lora.setTransmissionPower(LoraAS32::_21dBm);
    ok = true;
  }

  if (ok) {
    Serial.println("tx_power_command: " + String(power));
  }
}

//int TIMEOUT = 3000;
int timeout = 7000;

void dollar_command() {
  String command;

  if (parseString(command)) {
    String param;
    bool param_exist = parseString(param);

    //    LoraAS32::Mode original_mode = lora.getMode();
    //    lora.setMode(LoraAS32::Sleep);

    if (command.equals("air")) {
      air_speed_command(param);
    } else if (command.equals("power")) {
      tx_power_command(param);

    } else if (command.equals("load")) {
      if (lora.loadSetting()) {
        byte* parameter = lora.getParameter();
        Serial.print("load: ");
        for (int x = 0; x < 6; x++) {
          Serial.print((int)parameter[x]);
          Serial.print(' ');
        }
        Serial.println();
      } else {
        Serial.println("load failed");
      }
      lora.setMode(LoraAS32::Normal);

    } else if (command.equals("store")) {
      if (param.equals("sram")) {
        Serial.println("storeSettingToSram");
        if (!lora.storeSettingToSram()) {
          Serial.println("store failed");
        }
      } else if (param.equals("flash")) {
        Serial.println("storeSettingToFlash");
        if (!lora.storeSettingToFlash()) {
          Serial.println("store failed");
        }
      } else {
        Serial.println("store command failed: " + param);
      }
    } else if (command.equals("reset")) {
      Serial.println("reset");
      lora.reset();
    } else if (command.equals("mode")) {
      if ( param.equals("normal")) {
        lora.setMode(LoraAS32::Normal);
      } else if ( param.equals("sleep")) {
        lora.setMode(LoraAS32::Sleep);
      } else  if ( param.equals("read")) {
        LoraAS32::Mode original_mode = lora.getMode();
        Serial.println("mode: " + String(original_mode));
      }
    } else if (command.equals("wait")) {
      int wait_time = atoi(param.c_str());
      lora.setStoreWaitTime(wait_time);
    }
    else if (command.equals("timeout")) {
      if (param_exist) {
        timeout = atoi(param.c_str());
      }
      Serial.println("timeout: " + String(timeout));
    }else if (command.equals("binhex")) {
      if(param_exist) {
        print_binary_hex = param.equals("1");
      }
    }
  }


  char *arg = sCmd.next();
  if (arg != NULL) {
    Serial.println("$command: " + String(arg));

  }
}



/**
   可以設定功率 & 速度
   都一樣流程
   1. server通知改
   2. client回傳OK1, 此時server/client都改設定
   3. 改好, client 回傳OK2, server收到OK2, server回傳OK3
   4. 結束, 維持目前設定, 寫死設定

   # air
   # power
*/
void sharp_command() {
  String command;
  String param;

  if (parseString(command)) {
    if ( command.equals("air") | command.equals("power") ) {
      parseString(param);
      if (negotiation(command, param)) {
        Serial.println("negotiation OK");
      } else {
        Serial.println("negotiation NG");
      }
    } else  if ( command.equals("#")) {
      parseString(param);
      if ( param.equals("air")) {
        String param1;
        parseString(param1);
        air_speed_command_done(param1);
      }
      else {
        Serial.println("failed # # command");
      }

    }
  }
}

bool negotiation(String command, String param) {
  Serial1.setTimeout(timeout);

  String send_out = "# " + command + " " + param;
  Serial1.println(send_out);
  Serial.println(send_out);

  Serial.println("wait OK1");
  if ( Serial1.readStringUntil('\n').equals("OK1")) {
    int org_air_speed;// = lora.getAirSpeed();
    //改設定
    if ( command.equals("air")) {
      org_air_speed = lora.getAirSpeed();
      air_speed_command_done(param);
      //      delay(45);
      //      bool store_result = lora.storeSettingToSram();
      //      lora.setMode(LoraAS32::Normal);
      //      if (!store_result) {
      //        Serial.println("store to sram failed");
      //      }
    } else if ( command.equals("power")) { //power的話, 對方改就好, 自己只要等對方改完

    }
    Serial.println("wait OK2");
    String recv_string =  Serial1.readStringUntil('\n');
    if ( recv_string.equals("OK2")) {
      //成功
      Serial.println("send OK3");
      Serial1.println("OK3");
      return true;
    } else {
      Serial.println("recv string: " + recv_string);
      //      recv_string = Serial1.readString();
      //      Serial.println("recv string 2: " + recv_string);

      //失敗, 退回原設定
      if ( command.equals("air")) {
        lora.setAirSpeed(org_air_speed);
      } else {

      }
      lora.setMode(LoraAS32::Sleep);
      bool store_result = lora.storeSettingToSram();
      lora.setMode(LoraAS32::Normal);
    }
  }
  return false;
}

void tx_command() {
  String cmd;
  if (parseString(cmd)) {
    String output = cmd;
    while (parseString(cmd)) {
      output += " " + cmd;
    }

    Serial1.println(output);
    //    Serial1.write(cmd.c_str());
    Serial.println("tx: " + output);
  } else {
    Serial.println("no command");
  }

}



// This gets set as the default handler, and gets called when no other command matches.
void unrecognized(const char *command) {
  Serial.println("What?");
}

bool parseInteger(int* integer) {
  const char *arg = sCmd.next();
  if (arg != NULL) {
    *integer =  atoi(arg);
    return true;
  } else {
    return false;
  }
}

bool parseString(String& string) {
  const char *arg = sCmd.next();
  if (arg != NULL) {
    string = arg;
    return true;
  } else {
    string = "";
    return false;
  }
}
