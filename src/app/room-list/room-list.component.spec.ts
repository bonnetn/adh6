import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomListComponent } from './room-list.component';
import { RouterTestingModule } from '@angular/router/testing';
import { ApiModule } from '../api/api.module';

describe('RoomListComponent', () => {
  let component: RoomListComponent;
  let fixture: ComponentFixture<RoomListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RoomListComponent ]
      imports: [
        ApiModule,
        RouterTestingModule,
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RoomListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
