\version "2.22" 
\include "lilypond-book-preamble.ly"
    
color = #(define-music-function (parser location color) (string?) #{
        \once \override NoteHead #'color = #(x11-color color)
        \once \override Stem #'color = #(x11-color color)
        \once \override Rest #'color = #(x11-color color)
        \once \override Beam #'color = #(x11-color color)
     #})
    
\header { } 
\score  { 
 \new Voice { \new Voice { \clef "treble" 
                \time 4/4
                r 4  
                r 8.  
                d'' 4  
                d'' 4  
                r 8.  
                r 8  
                cis, 4  
                d, 4  
                r 8  
                 } 
               
 
           } 
         
 
  } 
 
\paper { }
\layout {
  \context {
    \RemoveEmptyStaffContext
    \override VerticalAxisGroup #'remove-first = ##t
  }
 }
 
