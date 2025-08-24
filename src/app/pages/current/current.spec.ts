import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Current } from './current';

describe('Current', () => {
  let component: Current;
  let fixture: ComponentFixture<Current>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Current]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Current);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
