import { Component } from '@angular/core';

@Component({
  selector: 'app-connection-helper',
  templateUrl: './connection-helper.component.html',
  styleUrl: './connection-helper.component.scss'
})
export class ConnectionHelperComponent {
  ssh_command = 'ssh -L 15672:127.0.0.1:15672 -L 5672:127.0.0.1:5672 -L 27017:127.0.0.1:27017 node103';
}
