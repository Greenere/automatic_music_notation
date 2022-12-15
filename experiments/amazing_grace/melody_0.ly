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
 \new Voice { \new Voice { \clef "alto" 
                \time 4/4
                cis 4  
                dis 4  
                fis 2  
                fis 2  
                gis 4  
                a 4  
                fis 4  
                ais' 4  
                b 2  
                d 4  
                gis 4  
                a 4  
                r 16  
                g' 4  
                g 2  
                a 4  
                cis' 4  
                dis 4  
                d 2  
                cis 4  
                d 4  
                f 4  
                g 4  
                g 1  
                ais 4  
                g 4  
                b 4  
                r 16  
                r 16  
                gis 4  
                a 4  
                dis' 4  
                d' 1  
                d' 2  
                r 8  
                r 16  
                ais 4  
                b 4  
                cis' 4  
                d'' 2  
                e'' 4  
                r 16  
                ais 1  
                c'' 4  
                r 16  
                gis 4  
                a 4  
                g 2.  
                a 4  
                r 16  
                dis 2  
                d 4  
                d 2  
                r 16  
                gis 4  
                d 4  
                g 4  
                fis 4  
                g 4  
                r 16  
                b 4  
                b, 4  
                ais 4  
                ais 4  
                b' 4  
                r 16  
                g 4  
                gis 2  
                g 2  
                fis 4  
                g 4  
                r 8  
                r 16  
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
 
