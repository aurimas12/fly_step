import { Component,computed,EventEmitter,Input,input, Output,output} from '@angular/core';
import { DUMMY_USERS } from '../dummy-users';

const randomIndex=Math.floor(Math.random() *DUMMY_USERS.length)

@Component({
  selector: 'app-user',
  standalone:true,
  templateUrl: './user.component.html',
  styleUrl: './user.component.css'
})
export class UserComponent {
  @Input({required:true}) id!:string
  @Input({required:true}) avatar!:string;
  @Input({required:true}) name!:string;
  @Output() select=new EventEmitter();
  // select=output<string>();
  get imagePath(){
    return 'assets/users/' + this.avatar
  }
  onSelectUser(){
    this.select.emit(this.id);
  }
}
