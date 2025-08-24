import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NextWeek } from './next-week';

describe('NextWeek', () => {
  let component: NextWeek;
  let fixture: ComponentFixture<NextWeek>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NextWeek]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NextWeek);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
