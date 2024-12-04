import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ConnectionHelperComponent } from './connection-helper/connection-helper.component';

@Component({
  selector: 'app-rabbitmq',
  templateUrl: './rabbitmq.component.html',
  styleUrl: './rabbitmq.component.scss'
})
export class RabbitmqComponent {
  constructor(
    private dialog: MatDialog,
  ) { }

  openDialog() {
    this.dialog.open(ConnectionHelperComponent, {
      maxWidth: '100%',
    });
  }
}
